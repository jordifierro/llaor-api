from django.conf.urls import url
from llaor.views import ViewWrapper
from dictionary.views import DictionaryView

urlpatterns = [
    url(r'^dictionary/words/$', ViewWrapper.as_view(view=DictionaryView), name='dictionary'),
]
