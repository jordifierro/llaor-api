import json
from mock import patch

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from dictionary.models import Definition


class AllWordsViewTestCase(TestCase):

    @patch('dictionary.navigators.Navigator._get_full_uri')
    def test_returns_list_of_word_with_uri_and_200(self, get_full_uri):
        Definition.objects.create(word="word_a", meaning="any", semantic_group=1,
                                  source="test data", public=True)
        Definition.objects.create(word="word_b", meaning="any", semantic_group=1,
                                  source="test data", public=True)

        def fake_full_uri(x):
            return "full-uri{}".format(x)
        get_full_uri.side_effect = fake_full_uri

        response = Client().get(reverse('words'))

        assert response.status_code == 200
        body = json.loads(response.content)
        assert body == [
                           {
                               'word': 'word_a',
                               'uri': 'full-uri{}word_a'.format(reverse('words'))
                           },
                           {
                               'word': 'word_b',
                               'uri': 'full-uri{}word_b'.format(reverse('words'))
                           },
                       ]

        Definition.objects.all().delete()


class WordViewTestCase(TestCase):

    @patch('dictionary.navigators.Navigator._get_full_uri')
    def test_returns_list_of_word_meanings_and_200(self, get_full_uri):
        Definition.objects.create(word="target", scientific="sc", type="ty", meaning="desc",
                                  extra_info="e_i", synonyms="a, b", related="c, d")
        Definition.objects.create(word="target", scientific="lorem", type="noun", meaning="word meaning",
                                  extra_info="none")

        def fake_full_uri(x):
            return "full-uri{}".format(x)
        get_full_uri.side_effect = fake_full_uri

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
                                       'uri': 'full-uri{}a'.format(reverse('words'))
                                   },
                                   {
                                       'word': 'b',
                                       'uri': 'full-uri{}b'.format(reverse('words'))
                                   },
                               ],
                               'related_words': [
                                   {
                                       'word': 'c',
                                       'uri': 'full-uri{}c'.format(reverse('words'))
                                   },
                                   {
                                       'word': 'd',
                                       'uri': 'full-uri{}d'.format(reverse('words'))
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
