from elasticsearch.exceptions import NotFoundError
import logging

from django.test import TestCase

from dictionary.factories import create_word_search_repo
from dictionary.repositories import WordRepo
from dictionary.models import Definition
from dictionary.entities import WordMeanings, Meaning


class GetForWordTestCase(TestCase):

    def test_no_meanings_returns_empty_list(self):
        GetForWordTestCase.ScenarioMaker() \
                .given_a_word() \
                .given_no_meanings() \
                .when_get_word() \
                .then_an_empty_list_should_be_returned()

    def test_meaning_is_correctly_parsed(self):
        GetForWordTestCase.ScenarioMaker() \
                .given_a_word() \
                .given_a_meaning_for_that_word() \
                .when_get_word() \
                .then_meaning_should_be_correctly_parsed()

    def test_private_meaning_should_not_be_returned(self):
        GetForWordTestCase.ScenarioMaker() \
                .given_a_word() \
                .given_a_meaning_for_that_word(public=False) \
                .when_get_word() \
                .then_an_empty_list_should_be_returned()

    def test_two_meanings_should_be_returned_sorted_by_semantic_group(self):
        GetForWordTestCase.ScenarioMaker() \
                .given_a_word() \
                .given_two_meanings_for_that_word() \
                .when_get_word() \
                .then_both_should_be_retrieved_in_proper_order()

    class ScenarioMaker(object):

        def __init__(self):
            self.word = None
            self.meanings = None
            self.response = None
            self.orm_definition = None
            self.orm_definition_2 = None

        def given_a_word(self):
            self.word = "sample"

            return self

        def given_no_meanings(self):
            return self

        def given_a_meaning_for_that_word(self, public=True):
            self.orm_definition = Definition.objects.create(word=self.word, phonetic="ph", scientific="lorem",
                                                            type="noun", meaning="A small part",
                                                            extra_info="Typical word",
                                                            private_notes="secret", synonyms="taste, specimen",
                                                            related="data, analysis", origin="england",
                                                            semantic_field="statistics", semantic_group=1,
                                                            source="test data", reviewed=True, public=public)

            return self

        def given_two_meanings_for_that_word(self):
            self.orm_definition = Definition.objects.create(word=self.word, phonetic="ph", scientific="lorem",
                                                            type="noun", meaning="A small part",
                                                            extra_info="Typical word",
                                                            private_notes="secret", synonyms="taste, specimen",
                                                            related="data, analysis", origin="england",
                                                            semantic_field="statistics", semantic_group=1,
                                                            source="test data", reviewed=True, public=True)

            self.orm_definition_2 = Definition.objects.create(word=self.word, phonetic="zh", scientific="ipsum",
                                                              type="verb", meaning="Take a sample",
                                                              extra_info="Non typical word",
                                                              private_notes="secret", synonyms="try, test",
                                                              related="data, analysis", origin="england",
                                                              semantic_field="statistics", semantic_group=2,
                                                              source="test data", reviewed=True, public=True)

            return self

        def when_get_word(self):
            self.response = WordRepo().get_word_meanings(self.word)

            return self

        def then_an_empty_list_should_be_returned(self):
            assert self.response == WordMeanings(self.word, [])

            return self

        def then_meaning_should_be_correctly_parsed(self):
            assert self.response.word == self.word
            self._assert_orm_definition_and_meaning_are_equal(orm_definition=self.orm_definition,
                                                              meaning=self.response.meanings[0])

            return self

        def then_both_should_be_retrieved_in_proper_order(self):
            assert self.response.word == self.word
            self._assert_orm_definition_and_meaning_are_equal(orm_definition=self.orm_definition,
                                                              meaning=self.response.meanings[0])
            self._assert_orm_definition_and_meaning_are_equal(orm_definition=self.orm_definition_2,
                                                              meaning=self.response.meanings[1])

            return self

        def _assert_orm_definition_and_meaning_are_equal(self, orm_definition, meaning):
            assert orm_definition.scientific == meaning.scientific
            assert orm_definition.type == meaning.type
            assert orm_definition.meaning == meaning.description
            assert orm_definition.extra_info == meaning.extra_info
            assert orm_definition.synonyms.split(', ') == meaning.synonym_words
            assert orm_definition.related.split(', ') == meaning.related_words


class GetAllWordsTestCase(TestCase):

    def test_returns_words_with_their_meanings(self):
        GetAllWordsTestCase.ScenarioMaker() \
                .given_a_definition(word='word_a', scientific='s', type='t', meaning='one',
                                 extra_info='x', synonyms="a, b 2", related="c 1, b 2", public=True) \
                .given_a_definition(word='word_a', scientific='r', type='u', meaning='two',
                                 extra_info='y', synonyms="x, b2", related="c1, w2", public=True) \
                .given_a_definition(word='word_b', scientific='s', type='q', meaning='new',
                                 extra_info='o', synonyms="x, b2", related="c1, w2", public=True) \
                .when_get_all_words() \
                .then_should_return([
                    WordMeanings(word='word_a', meanings=[
                        Meaning('s', 't', 'one', 'x', ['a', 'b 2'], ['c 1', 'b 2']),
                        Meaning('r', 'u', 'two', 'y', ['x', 'b2'], ['c1', 'w2'])
                    ]),
                    WordMeanings(word='word_b', meanings=[
                        Meaning('s', 'q', 'new', 'o', ['x', 'b2'], ['c1', 'w2'])
                    ]),
                ])

    class ScenarioMaker(object):

        def given_a_definition(self, word, scientific, type, meaning,
                               extra_info, synonyms, related, public):
            Definition.objects.create(word=word, scientific=scientific, type=type, meaning=meaning,
                                      extra_info=extra_info, synonyms=synonyms, related=related, public=public)
            return self

        def when_get_all_words(self):
            self.response = WordRepo().get_all_words_meanings()
            return self

        def then_should_return(self, response):
            assert self.response == response
            return self


class WordSearchRepoTestCase(TestCase):

    def test_search_by_first_letter(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('a', [])) \
                .given_a_word(WordMeanings('ahola', [])) \
                .given_a_word(WordMeanings('adeu', [])) \
                .given_a_word(WordMeanings('baaa', [])) \
                .given_a_word(WordMeanings('xyz', [])) \
                .when_index_everything_and_search_by_first_letter('a') \
                .then_should_return(['a', 'adeu', 'ahola'])

    def test_search_by_first_letter_with_no_matches(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('baaa', [])) \
                .given_a_word(WordMeanings('xyz', [])) \
                .when_index_everything_and_search_by_first_letter('a') \
                .then_should_return([])

    class TestScenario:

        def __init__(self):
            self.repo = create_word_search_repo()
            try:
                self.repo._delete_word_index()
            except NotFoundError:
                pass
            self.repo._create_word_index()
            self.words = []
            logging.getLogger('elasticsearch').setLevel(logging.ERROR)

        def given_a_word(self, word):
            self.words.append(word)
            return self

        def when_index_everything_and_search_by_first_letter(self, first_letter):
            for word in self.words:
                self.repo.index_word(word)
            self.repo._refresh_word_index()
            self.result = self.repo.search_words_by_first_letter(first_letter)
            return self

        def then_should_return(self, result):
            assert self.result == result
            return self
