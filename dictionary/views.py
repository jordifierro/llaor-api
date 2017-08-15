from dictionary.serializers import MeaningSerializer


class AllWordsView(object):

    def __init__(self, word_repo, navigator):
        self.word_repo = word_repo
        self.navigator = navigator

    def get(self):
        words = self.word_repo.get_all_words()
        serialized_words = [{'word': word, 'uri': self.navigator.get_word_uri(word)} for word in words]

        body = serialized_words
        status = 200
        return body, status


class WordView(object):

    def __init__(self, word_repo, navigator):
        self.word_repo = word_repo
        self.navigator = navigator

    def get(self, word):
        meanings = self.word_repo.get_meanings_for_word(word)

        body = MeaningSerializer.serialize_multiple(meanings, self.navigator)
        status = 200
        return body, status
