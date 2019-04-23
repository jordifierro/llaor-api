from dictionary.serializers import serialize_word_meanings, serialize_words_meanings


class AllWordsView(object):

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def get(self):
        words_meanings = self.word_repo.get_all_words_meanings()

        body = serialize_words_meanings(words_meanings)
        status = 200
        return body, status


class WordView(object):

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def get(self, word):
        word_meanings = self.word_repo.get_word_meanings(word)

        body = serialize_word_meanings(word_meanings)
        status = 200
        return body, status
