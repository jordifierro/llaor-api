from django.test import TestCase

from dictionary.repositories import MeaningRepo
from dictionary.models import Definition


class MeaningRepoTestCase(TestCase):

    def test_no_meanings_returns_empty_list(self):
        MeaningRepoTestCase.ScenarioMaker() \
                .given_a_word() \
                .given_no_meanings() \
                .when_get_meanings_for_the_word() \
                .then_an_empty_list_should_be_returned()

    def test_meaning_is_correctly_parsed(self):
        MeaningRepoTestCase.ScenarioMaker() \
                .given_a_word() \
                .given_a_meaning_for_that_word() \
                .when_get_meanings_for_the_word() \
                .then_meaning_should_be_correctly_parsed()

    def test_private_meaning_should_not_be_returned(self):
        MeaningRepoTestCase.ScenarioMaker() \
                .given_a_word() \
                .given_a_meaning_for_that_word(public=False) \
                .when_get_meanings_for_the_word() \
                .then_an_empty_list_should_be_returned()

    def test_two_meanings_should_be_returned_sorted_by_semantic_group(self):
        MeaningRepoTestCase.ScenarioMaker() \
                .given_a_word() \
                .given_two_meanings_for_that_word() \
                .when_get_meanings_for_the_word() \
                .then_both_should_be_retrieved_in_proper_order()

    class ScenarioMaker(object):

        def __init__(self):
            self.word = None
            self.meanings = None
            self.response = None
            self.orm_definition = None

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

        def when_get_meanings_for_the_word(self):
            self.response = MeaningRepo().get_meanings_for_word(self.word)

            return self

        def then_an_empty_list_should_be_returned(self):
            assert self.response == []

            return self

        def then_meaning_should_be_correctly_parsed(self):
            self._assert_orm_definition_and_meaning_are_equal(orm_definition=self.orm_definition,
                                                              meaning=self.response[0])

            return self

        def then_both_should_be_retrieved_in_proper_order(self):
            self._assert_orm_definition_and_meaning_are_equal(orm_definition=self.orm_definition,
                                                              meaning=self.response[0])
            self._assert_orm_definition_and_meaning_are_equal(orm_definition=self.orm_definition_2,
                                                              meaning=self.response[1])

            return self

        def _assert_orm_definition_and_meaning_are_equal(self, orm_definition, meaning):
            assert orm_definition.scientific == meaning.scientific
            assert orm_definition.type == meaning.type
            assert orm_definition.meaning == meaning.description
            assert orm_definition.extra_info == meaning.extra_info
            assert orm_definition.synonyms.split(', ') == meaning.synonym_words
            assert orm_definition.related.split(', ') == meaning.related_words
