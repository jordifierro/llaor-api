import itertools
from elasticsearch import NotFoundError as ElasticSearchNotFoundError

from dictionary.entities import Meaning, Word
from dictionary.models import Definition


class WordRepo(object):

    def get_all_words(self):
        definitions = Definition.objects.filter(public=True).order_by('word')

        words = []
        for key, group in itertools.groupby(definitions, key=lambda x:x.word):
            words.append(Word(key, [self.parse_meaning(definition) for definition in group]))

        return words

    def get_word(self, word):
        orm_definitions = Definition.objects.filter(word=word, public=True)

        meanings = [self.parse_meaning(orm_definition) for orm_definition in orm_definitions]

        return Word(word, meanings)

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
                    "_source": {"enabled": False},
                    "properties": {
                        "word": {"type": "keyword"},
                    }
                }
            }
        }
        self.elastic_client.indices.create(index=index, body=body)

    def _refresh_word_index(self):
        self.elastic_client.indices.refresh(index=WordSearchRepo.WORD_INDEX)

    def _delete_word_index(self):
        self.elastic_client.indices.delete(index=WordSearchRepo.WORD_INDEX)

    def index_word(self, word):
        doc = {
                'word': word.word,
              }
        self.elastic_client.index(index=WordSearchRepo.WORD_INDEX,
                                  doc_type=WordSearchRepo.WORD_DOC_TYPE,
                                  body=doc, id=word.word)

    def delete_word(self, word_word):
        try:
            self.elastic_client.delete(index=WordSearchRepo.WORD_INDEX,
                                       doc_type=WordSearchRepo.WORD_DOC_TYPE,
                                       id=word_word)
        except ElasticSearchNotFoundError:
            pass

    def search_words_by_first_letter(self, first_letter):
        search_query = {
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
