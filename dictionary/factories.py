from elasticsearch import Elasticsearch
import certifi
import datetime
import pytz

from django.conf import settings

from dictionary.repositories import WordRepo, WordSearchRepo
from dictionary.views import AllWordsView, WordView


def create_word_search_repo():
    if not settings.LOCAL_DEPLOY:
        return WordSearchRepo(Elasticsearch([settings.ELASTICSEARCH_URL],
                                            use_ssl=True, ca_certs=certifi.where()))
    else:
        return WordSearchRepo(Elasticsearch([settings.ELASTICSEARCH_URL]))


def create_word_repo():
    return WordRepo(create_word_search_repo())


def create_word_view(request):
    now = datetime.datetime.now(tz=pytz.timezone('Europe/Madrid'))
    days = now.day
    months = now.month
    years = now.year
    daily_random_hash = days + months * 100 + years * 10000
    return WordView(word_repo=create_word_repo(), daily_random_hash=daily_random_hash)


def create_all_words_view(request):
    return AllWordsView(word_repo=create_word_repo())
