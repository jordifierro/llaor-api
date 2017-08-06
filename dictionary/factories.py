from dictionary.repositories import MeaningRepo
from dictionary.navigators import Navigator
from dictionary.views import DictionaryView, WordView


class MeaningRepoFactory(object):

    @staticmethod
    def get():
        return MeaningRepo()


class NavigatorFactory(object):

    @staticmethod
    def get(request):
        return Navigator(request)


class WordViewFactory(object):

    @staticmethod
    def create(request):
        meaning_repo = MeaningRepoFactory.get()
        navigator = NavigatorFactory.get(request)
        return WordView(meaning_repo=meaning_repo, navigator=navigator)


class DictionaryViewFactory(object):

    @staticmethod
    def create(request):
        navigator = NavigatorFactory.get(request)
        return DictionaryView(navigator=navigator)
