from dictionary.serializers import MeaningSerializer


class AllWordsView(object):

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def get(self):
        words = self.word_repo.get_all_words()

        body = MeaningSerializer.serialize_words(words)
        status = 200
        return body, status


class WordView(object):

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def get(self, word):
        word_with_meanings = self.word_repo.get_word(word)

        body = MeaningSerializer.serialize_word(word_with_meanings)
        status = 200
        return body, status
