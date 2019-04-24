from elasticsearch.exceptions import NotFoundError
import logging

from django.test import TestCase

from llaor.exceptions import EntityNotFoundException
from dictionary.factories import create_word_search_repo
from dictionary.repositories import WordRepo
from dictionary.models import Definition
from dictionary.entities import WordMeanings, Meaning


class WordRepoTestCase(TestCase):

    def test_a_definition_returns_word_with_that_meaning(self):
        WordRepoTestCase.TestScenario() \
                .given_a_definition(word="piece", phonetic="ph", scientific="lorem", type="noun",
                                    meaning="A small part", extra_info="Typical word",
                                    private_notes="secret", synonyms="taste, specimen",
                                    related="data, analysis", origin="england",
                                    semantic_field="statistics", semantic_group=1,
                                    source="test data", reviewed=True, public=True) \
                .when_get_word_meanings("piece") \
                .then_should_return(WordMeanings(word="piece",
                                                 meanings=[Meaning(scientific="lorem", type="noun",
                                                                   description="A small part",
                                                                   extra_info="Typical word",
                                                                   synonym_words=["taste", "specimen"],
                                                                   related_words=["data", "analysis"])]))

    def test_no_definition_returns_entity_not_found(self):
        WordRepoTestCase.TestScenario() \
                .when_get_word_meanings("none") \
                .then_should_raise(EntityNotFoundException)

    def test_private_meaning_should_not_be_returned(self):
        WordRepoTestCase.TestScenario() \
                .given_a_definition(word="piece", phonetic="ph", scientific="lorem", type="noun",
                                    meaning="A small part", extra_info="Typical word",
                                    private_notes="secret", synonyms="taste, specimen",
                                    related="data, analysis", origin="england",
                                    semantic_field="statistics", semantic_group=1,
                                    source="test data", reviewed=True, public=True) \
                .given_a_definition(word="piece", phonetic="ph", scientific="lorem", type="noun",
                                    meaning="A small part", extra_info="Typical word",
                                    private_notes="secret", synonyms="taste, specimen",
                                    related="data, analysis", origin="england",
                                    semantic_field="statistics", semantic_group=1,
                                    source="test data", reviewed=True, public=False) \
                .when_get_word_meanings("piece") \
                .then_should_return(WordMeanings(word="piece",
                                                 meanings=[Meaning(scientific="lorem", type="noun",
                                                                   description="A small part",
                                                                   extra_info="Typical word",
                                                                   synonym_words=["taste", "specimen"],
                                                                   related_words=["data", "analysis"])]))

    def test_no_reviewed_meaning_should_not_be_returned(self):
        WordRepoTestCase.TestScenario() \
                .given_a_definition(word="piece", phonetic="ph", scientific="lorem", type="noun",
                                    meaning="A small part", extra_info="Typical word",
                                    private_notes="secret", synonyms="taste, specimen",
                                    related="data, analysis", origin="england",
                                    semantic_field="statistics", semantic_group=1,
                                    source="test data", reviewed=True, public=True) \
                .given_a_definition(word="piece", phonetic="ph", scientific="lorem", type="noun",
                                    meaning="A small part", extra_info="Typical word",
                                    private_notes="secret", synonyms="taste, specimen",
                                    related="data, analysis", origin="england",
                                    semantic_field="statistics", semantic_group=1,
                                    source="test data", reviewed=False, public=True) \
                .when_get_word_meanings("piece") \
                .then_should_return(WordMeanings(word="piece",
                                                 meanings=[Meaning(scientific="lorem", type="noun",
                                                                   description="A small part",
                                                                   extra_info="Typical word",
                                                                   synonym_words=["taste", "specimen"],
                                                                   related_words=["data", "analysis"])]))

    def test_two_meanings_should_be_returned_sorted_by_semantic_group(self):
        WordRepoTestCase.TestScenario() \
                .given_a_definition(word="piece", phonetic="ph2", scientific="lorem2", type="noun2",
                                    meaning="A small part2", extra_info="Typical word2",
                                    private_notes="secret2", synonyms="taste2, specimen2",
                                    related="data2, analysis2", origin="england2",
                                    semantic_field="statistics2", semantic_group=2,
                                    source="test data", reviewed=True, public=True) \
                .given_a_definition(word="piece", phonetic="ph", scientific="lorem", type="noun",
                                    meaning="A small part", extra_info="Typical word",
                                    private_notes="secret", synonyms="taste, specimen",
                                    related="data, analysis", origin="england",
                                    semantic_field="statistics", semantic_group=1,
                                    source="test data", reviewed=True, public=True) \
                .when_get_word_meanings("piece") \
                .then_should_return(WordMeanings(word="piece",
                                                 meanings=[Meaning(scientific="lorem", type="noun",
                                                                   description="A small part",
                                                                   extra_info="Typical word",
                                                                   synonym_words=["taste", "specimen"],
                                                                   related_words=["data", "analysis"]),
                                                           Meaning(scientific="lorem2", type="noun2",
                                                                   description="A small part2",
                                                                   extra_info="Typical word2",
                                                                   synonym_words=["taste2", "specimen2"],
                                                                   related_words=["data2", "analysis2"])]))

    def test_returns_words_with_their_meanings(self):
        WordRepoTestCase.TestScenario() \
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

    class TestScenario(object):

        def given_a_definition(self, word, phonetic="", scientific="", type="", meaning="", extra_info="",
                               private_notes="", synonyms=[], related=[], origin="", semantic_field="",
                               semantic_group=0, source="", reviewed=True, public=True):
            Definition.objects.create(word=word, phonetic=phonetic, scientific=scientific,
                                      type=type, meaning=meaning, extra_info=extra_info,
                                      private_notes=private_notes, synonyms=synonyms, related=related,
                                      origin=origin, semantic_field=semantic_field,
                                      semantic_group=semantic_group, source=source,
                                      reviewed=reviewed, public=public)
            return self

        def when_get_word_meanings(self, word):
            try:
                self.response = WordRepo().get_word_meanings(word)
            except Exception as e:
                self.error = e

            return self

        def when_get_all_words(self):
            self.response = WordRepo().get_all_words_meanings()
            return self

        def then_should_return(self, response):
            assert self.response == response
            return self

        def then_should_raise(self, error):
            assert type(self.error) is error
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
