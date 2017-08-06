from dictionary.models import Definition
from dictionary.repositories import MeaningRepo
from dictionary.serializers import MeaningSerializer


class DictionaryView(object):

    def get(self):
        words = Definition.objects.values('word').order_by('word')

        body = list(words)
        status = 200
        return body, status


class WordView(object):

    def get(self, word):
        meanings = MeaningRepo.get_meanings_for_word(word)

        body = MeaningSerializer.serialize_multiple(meanings)
        status = 200
        return body, status
