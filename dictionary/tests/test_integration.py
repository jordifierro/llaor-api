import json
from mock import patch

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from dictionary.models import Definition


class AllWordsViewTestCase(TestCase):

    def test_returns_list_of_word_with_uri_and_200(self):
        AllWordsViewTestCase.TestScenario() \
            .given_a_definition(word="word_a", meaning="any",
                                semantic_group=1, source="test data", public=True) \
            .given_a_definition(word="word_b", meaning="any", semantic_group=1,
                                source="test data", public=True) \
            .when_get_words() \
            .then_should_response(200, ['word_a', 'word_b'])
    
    class TestScenario:

        def given_a_definition(self, word, meaning, semantic_group, source, public):
            Definition.objects.create(word=word, meaning=meaning, semantic_group=semantic_group,
                                      source=source, public=public)
            return self
            
        def when_get_words(self):
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
    

    class TestScenario:

        def given_a_definition(self, word, scientific, type, meaning, extra_info, synonyms="", related=""):
            Definition.objects.create(word=word, scientific=scientific, type=type,
                                      meaning=meaning, extra_info=extra_info,
                                      synonyms=synonyms, related=related)
            return self
            
        def when_get_word(self, word):
            self.response = Client().get(reverse('word', kwargs={'word': word}))
            return self

        def then_should_response(self, status, body):
            assert self.response.status_code == status
            assert json.loads(self.response.content) == body
            return self
