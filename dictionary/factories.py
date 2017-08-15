from dictionary.repositories import WordRepo
from dictionary.navigators import Navigator
from dictionary.views import AllWordsView, WordView


class WordRepoFactory(object):

    @staticmethod
    def get():
        return WordRepo()


class NavigatorFactory(object):

    @staticmethod
    def get(request):
        return Navigator(request)


class WordViewFactory(object):

    @staticmethod
    def create(request):
        word_repo = WordRepoFactory.get()
        navigator = NavigatorFactory.get(request)
        return WordView(word_repo=word_repo, navigator=navigator)


class AllWordsViewFactory(object):

    @staticmethod
    def create(request):
        word_repo = WordRepoFactory.get()
        navigator = NavigatorFactory.get(request)
        return AllWordsView(word_repo=word_repo, navigator=navigator)
