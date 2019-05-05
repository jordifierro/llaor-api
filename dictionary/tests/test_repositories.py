from elasticsearch.exceptions import NotFoundError
import logging

from django.test import TestCase

from llaor.exceptions import EntityNotFoundException
from dictionary.factories import create_word_search_repo, create_word_repo
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
                .given_a_definition(word="loft", phonetic="ph2", scientific="lorem2", type="noun2",
                                    meaning="A small part2", extra_info="Typical word2",
                                    private_notes="secret2", synonyms="taste2, specimen2",
                                    related="data2, analysis2", origin="england2",
                                    semantic_field="statistics2", semantic_group=2,
                                    source="test data", reviewed=True, public=True) \
                .given_a_definition(word="loft", phonetic="ph", scientific="lorem", type="noun",
                                    meaning="A small part", extra_info="Typical word",
                                    private_notes="secret", synonyms="taste, specimen",
                                    related="data, analysis", origin="england",
                                    semantic_field="statistics", semantic_group=1,
                                    source="test data", reviewed=True, public=True) \
                .when_get_words_meanings(["piece", "loft"]) \
                .then_should_return([
                                     WordMeanings(word="piece",
                                                  meanings=[Meaning(scientific="lorem", type="noun",
                                                                    description="A small part",
                                                                    extra_info="Typical word",
                                                                    synonym_words=["taste", "specimen"],
                                                                    related_words=["data", "analysis"]),
                                                            Meaning(scientific="lorem2", type="noun2",
                                                                    description="A small part2",
                                                                    extra_info="Typical word2",
                                                                    synonym_words=["taste2", "specimen2"],
                                                                    related_words=["data2", "analysis2"])]),
                                     WordMeanings(word="loft",
                                                  meanings=[Meaning(scientific="lorem", type="noun",
                                                                    description="A small part",
                                                                    extra_info="Typical word",
                                                                    synonym_words=["taste", "specimen"],
                                                                    related_words=["data", "analysis"]),
                                                            Meaning(scientific="lorem2", type="noun2",
                                                                    description="A small part2",
                                                                    extra_info="Typical word2",
                                                                    synonym_words=["taste2", "specimen2"],
                                                                    related_words=["data2", "analysis2"])]),
                                                            ])

    def test_get_all_words_meanings(self):
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

    def test_search_by_first_letter(self):
        WordRepoTestCase.TestScenario() \
                .given_a_definition(word='a_word', scientific='s', type='t', meaning='one',
                                    extra_info='x', synonyms="a, b 2", related="c 1, b 2", public=True) \
                .given_a_definition(word='a_word', scientific='r', type='u', meaning='two',
                                    extra_info='y', synonyms="x, b2", related="c1, w2", public=True) \
                .given_a_definition(word='a', scientific='r', type='w', meaning='first',
                                    extra_info='q', synonyms="o, b9", related="c4, t2", public=True) \
                .given_a_definition(word='word_b', scientific='s', type='q', meaning='new',
                                    extra_info='o', synonyms="x, b2", related="c1, w2", public=True) \
                .given_a_definition(word='b_word', scientific='s', type='q', meaning='new',
                                    extra_info='o', synonyms="x, b2", related="c1, w2", public=True) \
                .given_everything_is_indexed() \
                .when_get_words_meanings_by_fisrt_letter('a') \
                .then_should_return([
                    WordMeanings(word='a', meanings=[
                        Meaning('r', 'w', 'first', 'q', ['o', 'b9'], ['c4', 't2'])
                    ]),
                    WordMeanings(word='a_word', meanings=[
                        Meaning('s', 't', 'one', 'x', ['a', 'b 2'], ['c 1', 'b 2']),
                        Meaning('r', 'u', 'two', 'y', ['x', 'b2'], ['c1', 'w2'])
                    ]),
                ])

    def test_get_word_meanings_random(self):
        WordRepoTestCase.TestScenario() \
                .given_a_definition(word='a_word', scientific='s', type='t', meaning='one',
                                    extra_info='x', synonyms="a, b 2", related="c 1, b 2", public=True) \
                .given_a_definition(word='a_word', scientific='r', type='u', meaning='two',
                                    extra_info='y', synonyms="x, b2", related="c1, w2", public=True) \
                .given_a_definition(word='word_b', scientific='s', type='q', meaning='new',
                                    extra_info='o', synonyms="x, b2", related="c1, w2", public=True) \
                .given_a_definition(word='word_b', scientific='p', type='m', meaning='old',
                                    extra_info='u', synonyms="w, b3", related="c8, w9", public=True) \
                .given_everything_is_indexed() \
                .when_get_random_word_meanings() \
                .then_should_return_one_of([
                    WordMeanings(word='a_word', meanings=[
                        Meaning('s', 't', 'one', 'x', ['a', 'b 2'], ['c 1', 'b 2']),
                        Meaning('r', 'u', 'two', 'y', ['x', 'b2'], ['c1', 'w2'])
                    ]),
                    WordMeanings(word='word_b', meanings=[
                        Meaning('s', 'q', 'new', 'o', ['x', 'b2'], ['c1', 'w2']),
                        Meaning('p', 'm', 'old', 'u', ['w', 'b3'], ['c8', 'w9'])
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

        def when_get_word_meanings(self, word):
            try:
                self.response = create_word_repo().get_word_meanings(word)
            except Exception as e:
                self.error = e

            return self

        def when_get_words_meanings(self, words):
            self.response = create_word_repo().get_words_meanings(words)
            return self

        def when_get_all_words(self):
            self.response = create_word_repo().get_all_words_meanings()
            return self

        def when_get_words_meanings_by_fisrt_letter(self, letter):
            self.response = create_word_repo().get_words_meanings_by_first_letter(letter)
            return self

        def when_get_random_word_meanings(self):
            self.response = create_word_repo().get_random_word_meanings()
            return self

        def then_should_return(self, response):
            assert self.response == response
            return self

        def then_should_return_one_of(self, possible_responses):
            assert self.response in possible_responses
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
                .given_everythin_is_indexed() \
                .when_search_by_first_letter('a') \
                .then_should_return(['a', 'adeu', 'ahola'])

    def test_search_by_first_letter_with_no_matches(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('baaa', [])) \
                .given_a_word(WordMeanings('xyz', [])) \
                .given_everythin_is_indexed() \
                .when_search_by_first_letter('a') \
                .then_should_return([])

    def test_get_random_word_returns_a_word(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('baaa', [])) \
                .given_a_word(WordMeanings('xyz', [])) \
                .given_everythin_is_indexed() \
                .when_get_random_word() \
                .then_should_return_one_of(['baaa', 'xyz'])

    def test_search_words_when_no_match(self):
        WordSearchRepoTestCase.TestScenario() \
                .when_search_word('any') \
                .then_should_return([])

    def test_search_words_matches_by_word(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('sabuda', [])) \
                .given_a_word(WordMeanings('assaumanyat', [])) \
                .given_everythin_is_indexed() \
                .when_search_word('sabuda') \
                .then_should_return(['sabuda'])

    def test_search_words_matches_with_hyphen(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('avenar-se', [])) \
                .given_everythin_is_indexed() \
                .when_search_word('avenar-se') \
                .then_should_return(['avenar-se'])

    def test_search_words_matches_with_accent(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('després', [])) \
                .given_everythin_is_indexed() \
                .when_search_word('després') \
                .then_should_return(['després'])

    def test_search_words_matches_by_root_word(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('mallar', [])) \
                .given_everythin_is_indexed() \
                .when_search_word('mallem') \
                .then_should_return(['mallar'])

    def test_search_words_matches_femenine_gender(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('encalamunat -da', [])) \
                .given_everythin_is_indexed() \
                .when_search_word('encalamunada') \
                .then_should_return(['encalamunat -da'])

    def test_search_words_matches_with_typo(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('panasca', [])) \
                .given_everythin_is_indexed() \
                .when_search_word('panaso') \
                .then_should_return(['panasca'])

    def test_search_words_matches_by_description(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('mallorquer', [Meaning('', '', 'la planta del blat de moro', '', [], [])])) \
                .given_everythin_is_indexed() \
                .when_search_word('blat') \
                .then_should_return(['mallorquer'])

    def test_search_words_matches_by_scientific(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('sègol', [Meaning('secale cereale', '', '', '', [], [])])) \
                .given_everythin_is_indexed() \
                .when_search_word('secale') \
                .then_should_return(['sègol'])

    def test_search_words_matches_by_synonyms(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('corna', [Meaning('', '', '', '', ['bana'], [])])) \
                .given_everythin_is_indexed() \
                .when_search_word('bana') \
                .then_should_return(['corna'])

    def test_search_words_matches_by_related(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('lliri blanc', [Meaning('', '', '', '', [], ['assutzena'])])) \
                .given_everythin_is_indexed() \
                .when_search_word('assutzena') \
                .then_should_return(['lliri blanc'])

    def test_search_words_boosts_word_over_meaning(self):
        WordSearchRepoTestCase.TestScenario() \
                .given_a_word(WordMeanings('cadell', [Meaning('', '', '', '', ['gosset'], [])])) \
                .given_a_word(WordMeanings('gosset', [Meaning('', '', '', '', ['cadell'], [])])) \
                .given_everythin_is_indexed() \
                .when_search_word('gosset') \
                .then_should_return(['gosset', 'cadell'])

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

        def given_everythin_is_indexed(self):
            for word in self.words:
                self.repo.index_word(word)
            self.repo._refresh_word_index()
            return self

        def when_search_by_first_letter(self, first_letter):
            self.result = self.repo.search_words_by_first_letter(first_letter)
            return self

        def when_get_random_word(self):
            self.result = self.repo.get_random_word()
            return self

        def when_search_word(self, text):
            self.result = self.repo.search_words(text)
            return self

        def then_should_return(self, result):
            assert self.result == result
            return self

        def then_should_return_one_of(self, word_options):
            assert self.result in word_options
            return self
