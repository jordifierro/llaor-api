from django.conf.urls import url
from llaor.views import ViewWrapper
from dictionary.factories import create_all_words_view, create_word_view

urlpatterns = [
    url(r'^words/$', ViewWrapper.as_view(view_creator_func=create_all_words_view), name='words'),
    url(r'^words/(?P<word>.+)$', ViewWrapper.as_view(view_creator_func=create_word_view), name='word'),
]
