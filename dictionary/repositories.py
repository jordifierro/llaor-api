import itertools
import random
from elasticsearch import NotFoundError as ElasticSearchNotFoundError
from django.db.models import Case, When

from llaor.exceptions import EntityNotFoundException
from dictionary.entities import Meaning, WordMeanings
from dictionary.models import Definition


class WordRepo(object):

    def __init__(self, word_search_repo):
        self.word_search_repo = word_search_repo

    def get_all_words_meanings(self):
        definitions = Definition.objects.filter(public=True).order_by('word')

        words = []
        for key, group in itertools.groupby(definitions, key=lambda x:x.word):
            words.append(WordMeanings(key, [self.parse_meaning(definition) for definition in group]))

        return words

    def get_word_meanings(self, word):
        orm_definitions = Definition.objects.filter(word=word) \
                                            .filter(public=True) \
                                            .filter(reviewed=True) \
                                            .order_by('semantic_group')

        if not orm_definitions:
            raise EntityNotFoundException()

        meanings = [self.parse_meaning(orm_definition) for orm_definition in orm_definitions]

        return WordMeanings(word, meanings)

    def get_words_meanings(self, words):
        preserved = Case(*[When(word=pk, then=pos) for pos, pk in enumerate(words)])
        orm_definitions = Definition.objects.filter(word__in=words) \
                                            .filter(public=True) \
                                            .filter(reviewed=True) \
                                            .order_by(preserved)

        words_meanings = []
        for key, group in itertools.groupby(orm_definitions, key=lambda x:x.word):
            meanings = [self.parse_meaning(definition) for definition in sorted(list(group), key=lambda x:x.semantic_group)]
            words_meanings.append(WordMeanings(key, meanings))

        return words_meanings

    def get_words_meanings_by_first_letter(self, letter):
        words = self.word_search_repo.search_words_by_first_letter(letter)
        return self.get_words_meanings(words)

    def search_words_meanings(self, text):
        words = self.word_search_repo.search_words(text)
        return self.get_words_meanings(words)

    def get_random_word_meanings(self, seed=None):
        word = self.word_search_repo.get_random_word(seed)
        return self.get_word_meanings(word)

    def parse_meaning(self, orm_definition):
        return Meaning(scientific=orm_definition.scientific,
                       type=orm_definition.type,
                       description=orm_definition.meaning,
                       extra_info=orm_definition.extra_info,
                       synonym_words=orm_definition.synonyms.split(', ') if orm_definition.synonyms else [],
                       related_words=orm_definition.related.split(', ') if orm_definition.related else [])


class WordSearchRepo(object):

    WORD_INDEX = 'word_index'
    WORD_DOC_TYPE = 'word'

    def __init__(self, elastic_client):
        self.elastic_client = elastic_client

    def _create_word_index(self):
        index = WordSearchRepo.WORD_INDEX
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 3,
                    "number_of_replicas": 1
                }
            },
            "mappings": {
                WordSearchRepo.WORD_DOC_TYPE: {
                    "_source": {
                        "enabled": False
                    },
                    "properties": {
                        "word": {
                            "type": "keyword"
                        },
                        "analyzed_word": {
                            "type": "text",
                            "analyzer": "catalan"
                        },
                        "other_text": {
                            "type": "text",
                            "analyzer": "catalan"
                        },
                    }
                }
            }
        }
        self.elastic_client.indices.create(index=index, body=body)

    def _refresh_word_index(self):
        self.elastic_client.indices.refresh(index=WordSearchRepo.WORD_INDEX)

    def _delete_word_index(self):
        self.elastic_client.indices.delete(index=WordSearchRepo.WORD_INDEX)

    def index_word(self, word_meanings):
        joined_text = ''
        for meaning in word_meanings.meanings:
            joined_meaning = '{} {} {} {}'.format(meaning.scientific,
                                                  meaning.description,
                                                  ' '.join(meaning.synonym_words),
                                                  ' '.join(meaning.related_words))
            joined_text = '{} {}'.format(joined_text, joined_meaning)
        doc = {
                'word': word_meanings.word,
                'analyzed_word': word_meanings.word,
                'other_text': joined_text
              }
        self.elastic_client.index(index=WordSearchRepo.WORD_INDEX,
                                  doc_type=WordSearchRepo.WORD_DOC_TYPE,
                                  body=doc, id=word_meanings.word)

    def delete_word(self, word_word):
        try:
            self.elastic_client.delete(index=WordSearchRepo.WORD_INDEX,
                                       doc_type=WordSearchRepo.WORD_DOC_TYPE,
                                       id=word_word)
        except ElasticSearchNotFoundError:
            pass

    def search_words_by_first_letter(self, first_letter):
        search_query = {
            "size": 200,
            "sort": [
                {
                    "word": {
                        "order": "asc"
                    }
                }
            ],
            "query": {
                "prefix": {
                    "word": first_letter
                }
            }
        }

        res = self.elastic_client.search(index=WordSearchRepo.WORD_INDEX, body=search_query)

        return [x['_id'] for x in res['hits']['hits']]

    def get_random_word(self, seed=None):
        if seed is None:
            seed = random.randint(1, 1000000)
        search_query = {
            "size": 1,
            "query": {
                "function_score": {
                    "functions": [
                        {
                            "random_score": {
                                "seed": str(seed)
                            }
                        }
                    ]
                }
            }
        }

        res = self.elastic_client.search(index=WordSearchRepo.WORD_INDEX, body=search_query)

        return [x['_id'] for x in res['hits']['hits']][0]

    def search_words(self, text):
        search_query = {
            "size": 50,
            "query": {
                "multi_match": {
                  "query": text,
                  "fields": ["word^5", "analyzed_word^5", "other_text"],
                  "fuzziness": "AUTO"
                }
            }
        }

        res = self.elastic_client.search(index=WordSearchRepo.WORD_INDEX, body=search_query)

        return [x['_id'] for x in res['hits']['hits']]
