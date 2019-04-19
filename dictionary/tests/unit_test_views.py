from mock import Mock

from dictionary.views import AllWordsView, WordView
from dictionary.entities import Meaning


class TestAllWordsView(object):

    def test_returns_list_of_word_with_uri_and_200(self):
        TestAllWordsView.TestScenario() \
                .given_a_word_repo_that_returns(["word_a", "word_b"]) \
                .when_get_all_words_view() \
                .then_should_response(200, [{'word': 'word_a'}, {'word': 'word_b'}])

    class TestScenario:

        def given_a_word_repo_that_returns(self, words):
            self.word_repo_mock = Mock()
            self.word_repo_mock.get_all_words.return_value = words
            return self

        def when_get_all_words_view(self):
            self.body, self.status = AllWordsView(word_repo=self.word_repo_mock).get()
            return self

        def then_should_response(self, status, body):
            assert self.status == status
            assert self.body == body
            return self


class TestWordView(object):

    def test_returns_list_of_word_meanings_and_200(self):
        meaning_a = Meaning(scientific='sc', type='ty', description='desc', extra_info='e_i',
                            synonym_words=['a', 'b'], related_words=['c', 'd'])
        meaning_b = Meaning(scientific='lorem', type='noun', description='word meaning', extra_info='none',
                            synonym_words=[], related_words=[])

        TestWordView.TestScenario() \
                .given_a_word_repo_that_returns([meaning_a, meaning_b]) \
                .when_get_word_view("Test") \
                .then_should_call_repo_get_meanings_for_word("Test") \
                .then_should_response(200, [
                           {
                               'scientific': 'sc',
                               'type': 'ty',
                               'description': 'desc',
                               'extra_info': 'e_i',
                               'synonym_words': [
                                   {
                                       'word': 'a',
                                   },
                                   {
                                       'word': 'b',
                                   },
                               ],
                               'related_words': [
                                   {
                                       'word': 'c',
                                   },
                                   {
                                       'word': 'd',
                                   },
                               ],
                           },
                           {
                               'scientific': 'lorem',
                               'type': 'noun',
                               'description': 'word meaning',
                               'extra_info': 'none',
                               'synonym_words': [],
                               'related_words': [],
                           },
                       ])


    class TestScenario:

        def given_a_word_repo_that_returns(self, words):
            self.word_repo_mock = Mock()
            self.word_repo_mock.get_meanings_for_word.return_value = words
            return self

        def when_get_word_view(self, word):
            self.body, self.status = WordView(word_repo=self.word_repo_mock).get(word=word)
            return self

        def then_should_call_repo_get_meanings_for_word(self, word):
            self.word_repo_mock.get_meanings_for_word.assert_called_once_with(word)
            return self

        def then_should_response(self, status, body):
            assert self.status == status
            assert self.body == body
            return self

