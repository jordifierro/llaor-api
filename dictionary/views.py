from dictionary.models import Definition
from dictionary.serializers import MeaningSerializer


class DictionaryView(object):

    def __init__(self, navigator):
        self.navigator = navigator

    def get(self):
        words = list(Definition.objects.values('word').order_by('word'))
        for word in words:
            word['uri'] = self.navigator.get_word_uri(word['word'])

        body = list(words)
        status = 200
        return body, status


class WordView(object):

    def __init__(self, navigator, meaning_repo):
        self.navigator = navigator
        self.meaning_repo = meaning_repo

    def get(self, word):
        meanings = self.meaning_repo.get_meanings_for_word(word)

        body = MeaningSerializer.serialize_multiple(meanings, self.navigator)
        status = 200
        return body, status
