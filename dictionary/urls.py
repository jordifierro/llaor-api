from django.conf.urls import url
from dictionary import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^dictionary/$', login_required(views.dictionary_list)),
    url(r'^dictionary/(?P<key>[\w-]+)/$', login_required(views.definition_detail)),
]
