class Meaning(object):

    def __init__(self, scientific, type, description, extra_info, synonym_words, related_words):
        self._scientific = scientific
        self._type = type
        self._description = description
        self._extra_info = extra_info
        self._synonym_words = synonym_words
        self._related_words = related_words

    @property
    def scientific(self):
        return self._scientific

    @property
    def type(self):
        return self._type

    @property
    def description(self):
        return self._description

    @property
    def extra_info(self):
        return self._extra_info

    @property
    def synonym_words(self):
        return self._synonym_words

    @property
    def related_words(self):
        return self._related_words
