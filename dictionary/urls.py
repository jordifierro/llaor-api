from django.conf.urls import url
from llaor.views import ViewWrapper
from dictionary.factories import AllWordsViewFactory, WordViewFactory

urlpatterns = [
    url(r'^words/$', ViewWrapper.as_view(factory=AllWordsViewFactory), name='words-list'),
    url(r'^words/(?P<word>.+)$', ViewWrapper.as_view(factory=WordViewFactory), name='word'),
]
