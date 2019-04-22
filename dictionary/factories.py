from elasticsearch import Elasticsearch

from django.conf import settings

from dictionary.repositories import WordRepo, WordSearchRepo
from dictionary.views import AllWordsView, WordView


def create_word_repo():
    return WordRepo()


def create_word_search_repo():
    return WordSearchRepo(Elasticsearch([settings.ELASTICSEARCH_URL]))


def create_word_view(request):
    return WordView(word_repo=create_word_repo())


def create_all_words_view(request):
    return AllWordsView(word_repo=create_word_repo())
