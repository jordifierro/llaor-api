import json
import logging
from mock import patch
from elasticsearch.exceptions import NotFoundError

from django.test import TestCase, tag, Client
from django.core.urlresolvers import reverse

from dictionary.models import Definition
from dictionary.factories import create_word_search_repo, create_word_repo


class AllWordsViewTestCase(TestCase):

    def test_returns_list_of_word_with_uri_and_200(self):
        AllWordsViewTestCase.TestScenario() \
            .given_a_definition(word="word_a", scientific="s", type="t", meaning="any",
                                extra_info="x", semantic_group=1, source="test data",
                                synonyms="a, b", related="x, z", public=True) \
            .given_a_definition(word="word_b", scientific="s", type="t", meaning="other",
                                extra_info="x", semantic_group=1, source="test data",
                                synonyms="a, b", related="x, z", public=True) \
            .when_get_words() \
            .then_should_response(200, [
                {
                    'word': 'word_a',
                    'meanings': [
                        {
                            'scientific': 's',
                            'type': 't',
                            'description': 'any',
                            'extra_info': 'x',
                            'synonym_words': ['a', 'b'],
                            'related_words': ['x', 'z']
                        }
                    ]
                },
                {
                    'word': 'word_b',
                    'meanings': [
                        {
                            'scientific': 's',
                            'type': 't',
                            'description': 'other',
                            'extra_info': 'x',
                            'synonym_words': ['a', 'b'],
                            'related_words': ['x', 'z']
                        }
                    ]
                }
            ])
    
    @tag('elasticsearch')
    def test_get_all_words_with_first_letter_query_param(self):
        AllWordsViewTestCase.TestScenario() \
            .given_a_definition(word="other", scientific="s", type="t", meaning="other",
                                extra_info="x", semantic_group=1, source="test data",
                                synonyms="a, b", related="x, z", public=True) \
            .given_a_definition(word="word_a", scientific="s", type="t", meaning="any",
                                extra_info="x", semantic_group=1, source="test data",
                                synonyms="a, b", related="x, z", public=True) \
            .given_a_definition(word="word_b", scientific="s", type="t", meaning="other",
                                extra_info="x", semantic_group=1, source="test data",
                                synonyms="a, b", related="x, z", public=True) \
            .given_a_definition(word="a", scientific="s", type="t", meaning="other",
                                extra_info="x", semantic_group=1, source="test data",
                                synonyms="a, b", related="x, z", public=True) \
            .given_everything_is_indexed() \
            .when_get_words(first_letter='w') \
            .then_should_response(200, [
                {
                    'word': 'word_a',
                    'meanings': [
                        {
                            'scientific': 's',
                            'type': 't',
                            'description': 'any',
                            'extra_info': 'x',
                            'synonym_words': ['a', 'b'],
                            'related_words': ['x', 'z']
                        }
                    ]
                },
                {
                    'word': 'word_b',
                    'meanings': [
                        {
                            'scientific': 's',
                            'type': 't',
                            'description': 'other',
                            'extra_info': 'x',
                            'synonym_words': ['a', 'b'],
                            'related_words': ['x', 'z']
                        }
                    ]
                }
            ])

    @tag('elasticsearch')
    def test_get_all_words_with_search_query_param(self):
        AllWordsViewTestCase.TestScenario() \
            .given_a_definition(word="other", scientific="s", type="t", meaning="other",
                                extra_info="x", semantic_group=1, source="test data",
                                synonyms="a, b", related="x, z", public=True) \
            .given_a_definition(word="word_a", scientific="s", type="t", meaning="any target",
                                extra_info="x", semantic_group=1, source="test data",
                                synonyms="a, b", related="x, z", public=True) \
            .given_a_definition(word="word_b", scientific="s", type="t", meaning="other target",
                                extra_info="x", semantic_group=1, source="test data",
                                synonyms="a, b", related="x, z", public=True) \
            .given_a_definition(word="a", scientific="s", type="t", meaning="other",
                                extra_info="x", semantic_group=1, source="test data",
                                synonyms="a, b", related="x, z", public=True) \
            .given_everything_is_indexed() \
            .when_get_words(search='target') \
            .then_should_response(200, [
                {
                    'word': 'word_a',
                    'meanings': [
                        {
                            'scientific': 's',
                            'type': 't',
                            'description': 'any target',
                            'extra_info': 'x',
                            'synonym_words': ['a', 'b'],
                            'related_words': ['x', 'z']
                        }
                    ]
                },
                {
                    'word': 'word_b',
                    'meanings': [
                        {
                            'scientific': 's',
                            'type': 't',
                            'description': 'other target',
                            'extra_info': 'x',
                            'synonym_words': ['a', 'b'],
                            'related_words': ['x', 'z']
                        }
                    ]
                }
            ])

    class TestScenario:

        def given_a_definition(self, word, scientific, type, meaning, extra_info,
                               semantic_group, source, synonyms, related, public):
            Definition.objects.create(word=word, scientific=scientific, type=type,
                                      meaning=meaning, extra_info=extra_info, 
                                      semantic_group=semantic_group, source=source,
                                      synonyms=synonyms, related=related, public=public)
            return self

        def given_everything_is_indexed(self):
            search_repo = create_word_search_repo()
            try:
                search_repo._delete_word_index()
            except NotFoundError:
                pass
            search_repo._create_word_index()
            all_words_meanings = create_word_repo().get_all_words_meanings()
            for word_meanings in all_words_meanings:
                search_repo.index_word(word_meanings)
            logging.getLogger('elasticsearch').setLevel(logging.ERROR)
            search_repo._refresh_word_index()
            return self
            
        def when_get_words(self, first_letter=None, search=None):
            if first_letter is not None:
                self.response = Client().get('{}?first_letter={}'.format(reverse('words'), first_letter))
            elif search is not None:
                self.response = Client().get('{}?search={}'.format(reverse('words'), search))
            else:
                self.response = Client().get(reverse('words'))
            return self

        def then_should_response(self, status, body):
            assert self.response.status_code == status
            assert json.loads(self.response.content) == body
            return self


class WordViewTestCase(TestCase):

    def test_returns_list_of_word_meanings_and_200(self):
        WordViewTestCase.TestScenario() \
                .given_a_definition(word="target", scientific="sc", type="ty", meaning="desc",
                                    extra_info="e_i", synonyms="a, b", related="c, d") \
                .given_a_definition(word="target", scientific="lorem", type="noun",
                                    meaning="word meaning", extra_info="none") \
                .when_get_word('target') \
                .then_should_response(200, {'word': 'target',
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
    
    @tag('elasticsearch')
    def test_random_word_returns_word_meaning(self):
        WordViewTestCase.TestScenario() \
                .given_a_definition(word="target", scientific="sc", type="ty", meaning="desc",
                                    extra_info="e_i", synonyms="a, b", related="c, d") \
                .given_a_definition(word="target", scientific="lorem", type="noun",
                                    meaning="word meaning", extra_info="none") \
                .given_everything_is_indexed() \
                .when_get_word('random') \
                .then_should_response(200, {'word': 'target',
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

        def given_a_definition(self, word, scientific, type, meaning, extra_info, synonyms="", related=""):
            Definition.objects.create(word=word, scientific=scientific, type=type,
                                      meaning=meaning, extra_info=extra_info,
                                      synonyms=synonyms, related=related)
            return self
            
        def given_everything_is_indexed(self):
            search_repo = create_word_search_repo()
            try:
                search_repo._delete_word_index()
            except NotFoundError:
                pass
            search_repo._create_word_index()
            all_words_meanings = create_word_repo().get_all_words_meanings()
            for word_meanings in all_words_meanings:
                search_repo.index_word(word_meanings)
            logging.getLogger('elasticsearch').setLevel(logging.ERROR)
            search_repo._refresh_word_index()
            return self
            
        def when_get_word(self, word):
            self.response = Client().get(reverse('word', kwargs={'word': word}))
            return self

        def then_should_response(self, status, body):
            assert self.response.status_code == status
            assert json.loads(self.response.content) == body
            return self
