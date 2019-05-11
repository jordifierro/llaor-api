from mock import Mock

from dictionary.views import AllWordsView, WordView
from dictionary.entities import Meaning, WordMeanings


class TestAllWordsView(object):

    def test_returns_list_of_word_with_uri_and_200(self):
        TestAllWordsView.TestScenario() \
                .given_a_word_repo_that_returns([
                    WordMeanings(word='word_a', meanings=[
                        Meaning('s', 't', 'one', 'x', ['a', 'b 2'], ['c 1', 'b 2']),
                        Meaning('r', 'u', 'two', 'y', ['x', 'b2'], ['c1', 'w2'])
                    ]),
                    WordMeanings(word='word_b', meanings=[
                        Meaning('s', 'q', 'new', 'o', ['x', 'b2'], ['c1', 'w2'])
                    ]),
                ]) \
                .when_get_all_words_view() \
                .then_should_call_repo_get_all_words_meanings() \
                .then_should_response(200, [
                    {
                        'word': 'word_a',
                        'meanings': [
                            {
                                'scientific': 's',
                                'type': 't',
                                'description': 'one',
                                'extra_info': 'x',
                                'synonym_words': ['a', 'b 2'],
                                'related_words': ['c 1', 'b 2']
                            },
                            {
                                'scientific': 'r',
                                'type': 'u',
                                'description': 'two',
                                'extra_info': 'y',
                                'synonym_words': ['x', 'b2'],
                                'related_words': ['c1', 'w2']
                            }
                        ]
                    },
                    {
                        'word': 'word_b',
                        'meanings': [
                            {
                                'scientific': 's',
                                'type': 'q',
                                'description': 'new',
                                'extra_info': 'o',
                                'synonym_words': ['x', 'b2'],
                                'related_words': ['c1', 'w2']
                            },
                        ]
                    },
                ])

    def test_search_by_first_letter_calls_get_all_words_by_first_letter(self):
        TestAllWordsView.TestScenario() \
                .given_a_word_repo_that_returns([
                    WordMeanings(word='word_a', meanings=[
                        Meaning('s', 't', 'one', 'x', ['a', 'b 2'], ['c 1', 'b 2']),
                        Meaning('r', 'u', 'two', 'y', ['x', 'b2'], ['c1', 'w2'])
                    ]),
                    WordMeanings(word='word_b', meanings=[
                        Meaning('s', 'q', 'new', 'o', ['x', 'b2'], ['c1', 'w2'])
                    ]),
                ]) \
                .when_get_all_words_view(first_letter='c') \
                .then_should_call_repo_get_words_meanings_by_first_letter('c') \
                .then_should_response(200, [
                    {
                        'word': 'word_a',
                        'meanings': [
                            {
                                'scientific': 's',
                                'type': 't',
                                'description': 'one',
                                'extra_info': 'x',
                                'synonym_words': ['a', 'b 2'],
                                'related_words': ['c 1', 'b 2']
                            },
                            {
                                'scientific': 'r',
                                'type': 'u',
                                'description': 'two',
                                'extra_info': 'y',
                                'synonym_words': ['x', 'b2'],
                                'related_words': ['c1', 'w2']
                            }
                        ]
                    },
                    {
                        'word': 'word_b',
                        'meanings': [
                            {
                                'scientific': 's',
                                'type': 'q',
                                'description': 'new',
                                'extra_info': 'o',
                                'synonym_words': ['x', 'b2'],
                                'related_words': ['c1', 'w2']
                            },
                        ]
                    },
                ])

    def test_search_calls_search_words_meanings(self):
        TestAllWordsView.TestScenario() \
                .given_a_word_repo_that_returns([
                    WordMeanings(word='word_a', meanings=[
                        Meaning('s', 't', 'one', 'x', ['a', 'b 2'], ['c 1', 'b 2']),
                        Meaning('r', 'u', 'two', 'y', ['x', 'b2'], ['c1', 'w2'])
                    ]),
                    WordMeanings(word='word_b', meanings=[
                        Meaning('s', 'q', 'new', 'o', ['x', 'b2'], ['c1', 'w2'])
                    ]),
                ]) \
                .when_get_all_words_view(search='text') \
                .then_should_call_repo_search_words_meanings('text') \
                .then_should_response(200, [
                    {
                        'word': 'word_a',
                        'meanings': [
                            {
                                'scientific': 's',
                                'type': 't',
                                'description': 'one',
                                'extra_info': 'x',
                                'synonym_words': ['a', 'b 2'],
                                'related_words': ['c 1', 'b 2']
                            },
                            {
                                'scientific': 'r',
                                'type': 'u',
                                'description': 'two',
                                'extra_info': 'y',
                                'synonym_words': ['x', 'b2'],
                                'related_words': ['c1', 'w2']
                            }
                        ]
                    },
                    {
                        'word': 'word_b',
                        'meanings': [
                            {
                                'scientific': 's',
                                'type': 'q',
                                'description': 'new',
                                'extra_info': 'o',
                                'synonym_words': ['x', 'b2'],
                                'related_words': ['c1', 'w2']
                            },
                        ]
                    },
                ])

    class TestScenario:

        def given_a_word_repo_that_returns(self, words):
            self.word_repo_mock = Mock()
            self.word_repo_mock.get_all_words_meanings.return_value = words
            self.word_repo_mock.get_words_meanings_by_first_letter.return_value = words
            self.word_repo_mock.search_words_meanings.return_value = words
            return self

        def when_get_all_words_view(self, first_letter=None, search=None):
            self.body, self.status = AllWordsView(word_repo=self.word_repo_mock) \
                                        .get(first_letter=first_letter, search=search)
            return self

        def then_should_call_repo_get_all_words_meanings(self):
            self.word_repo_mock.get_all_words_meanings.assert_called_once_with()
            return self

        def then_should_call_repo_get_words_meanings_by_first_letter(self, first_letter):
            self.word_repo_mock.get_words_meanings_by_first_letter.assert_called_once_with(first_letter)
            return self

        def then_should_call_repo_search_words_meanings(self, text):
            self.word_repo_mock.search_words_meanings.assert_called_once_with(text)
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
                .given_a_word_repo_that_returns(WordMeanings("Test", [meaning_a, meaning_b])) \
                .when_get_word_view("Test") \
                .then_should_call_repo_get_meanings_for_word("Test") \
                .then_should_response(200, {'word': 'Test', 
                    'meanings': [
                           {
                               'scientific': 'sc',
                               'type': 'ty',
                               'description': 'desc',
                               'extra_info': 'e_i',
                               'synonym_words': ['a', 'b'],
                               'related_words': ['c', 'd']
                           },
                           {
                               'scientific': 'lorem',
                               'type': 'noun',
                               'description': 'word meaning',
                               'extra_info': 'none',
                               'synonym_words': [],
                               'related_words': [],
                           },
                       ]})

    def test_if_word_is_random_retrieves_and_returns_random_word_meanings(self):
        meaning_a = Meaning(scientific='sc', type='ty', description='desc', extra_info='e_i',
                            synonym_words=['a', 'b'], related_words=['c', 'd'])
        meaning_b = Meaning(scientific='lorem', type='noun', description='word meaning', extra_info='none',
                            synonym_words=[], related_words=[])

        TestWordView.TestScenario() \
                .given_a_word_repo_that_returns_on_random(WordMeanings("Test", [meaning_a, meaning_b])) \
                .when_get_word_view("random") \
                .then_should_call_repo_get_random_word_meanings() \
                .then_should_response(200, {'word': 'Test', 
                    'meanings': [
                           {
                               'scientific': 'sc',
                               'type': 'ty',
                               'description': 'desc',
                               'extra_info': 'e_i',
                               'synonym_words': ['a', 'b'],
                               'related_words': ['c', 'd']
                           },
                           {
                               'scientific': 'lorem',
                               'type': 'noun',
                               'description': 'word meaning',
                               'extra_info': 'none',
                               'synonym_words': [],
                               'related_words': [],
                           },
                       ]})


    class TestScenario:

        def given_a_word_repo_that_returns(self, word_meanings):
            self.word_repo_mock = Mock()
            self.word_repo_mock.get_word_meanings.return_value = word_meanings
            return self

        def given_a_word_repo_that_returns_on_random(self, word_meanings):
            self.word_repo_mock = Mock()
            self.word_repo_mock.get_random_word_meanings.return_value = word_meanings
            return self

        def when_get_word_view(self, word):
            self.body, self.status = WordView(word_repo=self.word_repo_mock).get(word=word)
            return self

        def then_should_call_repo_get_meanings_for_word(self, word):
            self.word_repo_mock.get_word_meanings.assert_called_once_with(word)
            return self

        def then_should_call_repo_get_random_word_meanings(self):
            self.word_repo_mock.get_random_word_meanings.assert_called_once()
            return self

        def then_should_response(self, status, body):
            assert self.status == status
            assert self.body == body
            return self

