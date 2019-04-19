import json
from mock import patch

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from dictionary.models import Definition


class AllWordsViewTestCase(TestCase):

    def test_returns_list_of_word_with_uri_and_200(self):
        Definition.objects.create(word="word_a", meaning="any", semantic_group=1,
                                  source="test data", public=True)
        Definition.objects.create(word="word_b", meaning="any", semantic_group=1,
                                  source="test data", public=True)

        response = Client().get(reverse('words'))

        assert response.status_code == 200
        body = json.loads(response.content)
        assert body == [
                           {
                               'word': 'word_a',
                           },
                           {
                               'word': 'word_b',
                           },
                       ]

        Definition.objects.all().delete()


class WordViewTestCase(TestCase):

    def test_returns_list_of_word_meanings_and_200(self):
        Definition.objects.create(word="target", scientific="sc", type="ty", meaning="desc",
                                  extra_info="e_i", synonyms="a, b", related="c, d")
        Definition.objects.create(word="target", scientific="lorem", type="noun", meaning="word meaning",
                                  extra_info="none")

        response = Client().get(reverse('word', kwargs={'word': 'target'}))

        assert response.status_code == 200
        body = json.loads(response.content)
        assert body == [
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
                       ]

        Definition.objects.all().delete()
