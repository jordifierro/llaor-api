from dictionary.entities import Meaning
from dictionary.models import Definition


class MeaningRepo(object):

    def get_meanings_for_word(word):
        orm_definitions = Definition.objects.filter(word=word)

        meanings = []
        for definition in orm_definitions:
            meaning = Meaning(scientific=definition.scientific,
                              type=definition.type,
                              description=definition.meaning,
                              extra_info=definition.extra_info,
                              synonym_words=definition.synonyms.split(', ') if definition.synonyms else [],
                              related_words=definition.related.split(', ') if definition.related else [])
            meanings.append(meaning)

        return meanings
