from dictionary.entities import Meaning, Word
from dictionary.models import Definition


class WordRepo(object):

    def get_all_words(self):
        words_queryset = Definition.objects.filter(public=True).values('word').order_by('word').distinct()
        return [word['word'] for word in words_queryset]

    def get_word(self, word):
        orm_definitions = Definition.objects.filter(word=word, public=True)

        meanings = []
        for definition in orm_definitions:
            meaning = Meaning(scientific=definition.scientific,
                              type=definition.type,
                              description=definition.meaning,
                              extra_info=definition.extra_info,
                              synonym_words=definition.synonyms.split(', ') if definition.synonyms else [],
                              related_words=definition.related.split(', ') if definition.related else [])
            meanings.append(meaning)

        return Word(word, meanings)
