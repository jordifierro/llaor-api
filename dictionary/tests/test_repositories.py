from django.test import TestCase

from dictionary.repositories import WordRepo
from dictionary.models import Definition
from dictionary.entities import Word


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
            self.response = WordRepo().get_word(self.word)

            return self

        def then_an_empty_list_should_be_returned(self):
            assert self.response == Word(self.word, [])

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

    def test_word_with_no_meanings_returns_empty_list(self):
        GetAllWordsTestCase.ScenarioMaker() \
                .given_a_word() \
                .given_no_meanings() \
                .when_get_all_words() \
                .then_an_empty_list_should_be_returned()

    def test_word_with_multiple_meanings_returns_word(self):
        GetAllWordsTestCase.ScenarioMaker() \
                .given_a_word() \
                .given_multiple_meanings_for_each_word() \
                .when_get_all_words() \
                .then_word_should_be_returned()

    def test_multiple_words_sorts_them_alphabetically(self):
        GetAllWordsTestCase.ScenarioMaker() \
                .given_multiple_words() \
                .given_multiple_meanings_for_each_word() \
                .when_get_all_words() \
                .then_response_should_retrieve_words_sorted_alphabetically()

    class ScenarioMaker(object):

        def __init__(self):
            self.words = None
            self.response = None

        def given_a_word(self):
            self.words = ["sample"]

            return self

        def given_multiple_words(self):
            self.words = ["sample", "abc"]

            return self

        def given_no_meanings(self):
            return self

        def given_multiple_meanings_for_each_word(self):
            for word in self.words:
                Definition.objects.create(word=word, phonetic="ph", scientific="lorem",
                                          type="noun", meaning="A small part",
                                          extra_info="Typical word",
                                          private_notes="secret", synonyms="taste, specimen",
                                          related="data, analysis", origin="england",
                                          semantic_field="statistics", semantic_group=1,
                                          source="test data", reviewed=True, public=True)

                Definition.objects.create(word=word, phonetic="zh", scientific="ipsum",
                                          type="verb", meaning="Take a sample",
                                          extra_info="Non typical word",
                                          private_notes="secret", synonyms="try, test",
                                          related="data, analysis", origin="england",
                                          semantic_field="statistics", semantic_group=2,
                                          source="test data", reviewed=True, public=True)

            return self

        def when_get_all_words(self):
            self.response = WordRepo().get_all_words()

            return self

        def then_an_empty_list_should_be_returned(self):
            assert self.response == []

            return self

        def then_word_should_be_returned(self):
            assert self.words == self.response

            return self

        def then_response_should_retrieve_words_sorted_alphabetically(self):
            assert sorted(self.words) == self.response

            return self
