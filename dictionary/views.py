from dictionary.models import Definition


class DictionaryView(object):

    def get(self):
        words = Definition.objects.values('word').order_by('word')

        body = list(words)
        status = 200
        return body, status
