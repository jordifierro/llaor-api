from dictionary.repositories import WordRepo
from dictionary.navigators import Navigator
from dictionary.views import AllWordsView, WordView


def create_word_repo():
    return WordRepo()


def create_navigator(request):
    return Navigator(request)


def create_word_view(request):
    return WordView(word_repo=create_word_repo(), navigator=create_navigator(request))


def create_all_words_view(request):
    return AllWordsView(word_repo=create_word_repo(), navigator=create_navigator(request))
