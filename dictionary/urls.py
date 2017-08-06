from django.conf.urls import url
from llaor.views import ViewWrapper
from dictionary.factories import DictionaryViewFactory, WordViewFactory

urlpatterns = [
    url(r'^dictionary/words/$', ViewWrapper.as_view(factory=DictionaryViewFactory), name='dictionary'),
    url(r'^dictionary/words/(?P<word>.+)$', ViewWrapper.as_view(factory=WordViewFactory), name='word'),
]
