from django.urls import reverse


class Navigator(object):

    def __init__(self, request):
        self.request = request

    def get_word_uri(self, word):
        relative_uri = reverse('word', kwargs={'word': word})
        return self._get_full_uri(relative_uri)

    def _get_full_uri(self, relative_uri):
        return self.request.build_absolute_uri(relative_uri)
