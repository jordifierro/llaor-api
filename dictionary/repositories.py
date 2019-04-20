import itertools

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
