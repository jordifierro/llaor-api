from dictionary.serializers import serialize_word_meanings, serialize_words_meanings


class AllWordsView(object):

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def get(self, first_letter=None):
        if first_letter is None:
            words_meanings = self.word_repo.get_all_words_meanings()
        else:
            words_meanings = self.word_repo.get_words_meanings_by_first_letter(first_letter)

        body = serialize_words_meanings(words_meanings)
        status = 200
        return body, status


class WordView(object):

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def get(self, word):
        if word == 'random':
            word_meanings = self.word_repo.get_random_word_meanings()
        else:
            word_meanings = self.word_repo.get_word_meanings(word)

        body = serialize_word_meanings(word_meanings)
        status = 200
        return body, status
