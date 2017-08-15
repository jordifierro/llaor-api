from mock import Mock

from dictionary.views import AllWordsView, WordView
from dictionary.entities import Meaning


class TestAllWordsView(object):

    def test_returns_list_of_word_with_uri_and_200(self):
        navigator = Mock()
        navigator.get_word_uri = lambda x: "uri-word/{}".format(x)

        word_repo_mock = Mock()
        word_repo_mock.get_all_words.return_value = ["word_a", "word_b"]

        body, status = AllWordsView(word_repo=word_repo_mock, navigator=navigator).get()

        assert status == 200
        assert body == [
                           {
                               'word': 'word_a',
                               'uri': 'uri-word/word_a'
                           },
                           {
                               'word': 'word_b',
                               'uri': 'uri-word/word_b'
                           },
                       ]


class TestWordView(object):

    def test_returns_list_of_word_meanings_and_200(self):
        navigator = Mock()
        navigator.get_word_uri = lambda x: "uri-word/{}".format(x)

        meaning_a = Meaning(scientific='sc', type='ty', description='desc', extra_info='e_i',
                            synonym_words=['a', 'b'], related_words=['c', 'd'])
        meaning_b = Meaning(scientific='lorem', type='noun', description='word meaning', extra_info='none',
                            synonym_words=[], related_words=[])
        word_repo_mock = Mock()
        word_repo_mock.get_meanings_for_word.return_value = [meaning_a, meaning_b]

        body, status = WordView(word_repo=word_repo_mock, navigator=navigator).get(word="Test")

        word_repo_mock.get_meanings_for_word.assert_called_once_with("Test")
        assert status == 200
        assert body == [
                           {
                               'scientific': 'sc',
                               'type': 'ty',
                               'description': 'desc',
                               'extra_info': 'e_i',
                               'synonym_words': [
                                   {
                                       'word': 'a',
                                       'uri': 'uri-word/a'
                                   },
                                   {
                                       'word': 'b',
                                       'uri': 'uri-word/b'
                                   },
                               ],
                               'related_words': [
                                   {
                                       'word': 'c',
                                       'uri': 'uri-word/c'
                                   },
                                   {
                                       'word': 'd',
                                       'uri': 'uri-word/d'
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
                       ]
