from dictionary.serializers import MeaningSerializer


class AllWordsView(object):

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def get(self):
        words = self.word_repo.get_all_words()
        serialized_words = [{'word': word} for word in words]

        body = serialized_words
        status = 200
        return body, status


class WordView(object):

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def get(self, word):
        meanings = self.word_repo.get_meanings_for_word(word)

        body = MeaningSerializer.serialize_multiple(meanings)
        status = 200
        return body, status
