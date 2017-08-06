from django.conf.urls import url
from llaor.views import ViewWrapper
from dictionary.views import DictionaryView, WordView

urlpatterns = [
    url(r'^dictionary/words/$', ViewWrapper.as_view(view=DictionaryView), name='dictionary'),
    url(r'^dictionary/words/(?P<word>.+)$', ViewWrapper.as_view(view=WordView), name='word'),
]
