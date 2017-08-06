class MeaningSerializer(object):

    @staticmethod
    def serialize(meaning, navigator):
        return {
            'scientific': meaning.scientific,
            'type': meaning.type,
            'description': meaning.description,
            'extra_info': meaning.extra_info,
            'synonym_words': [{'word': word, 'uri': navigator.get_word_uri(word)} for word in meaning.synonym_words],
            'related_words': [{'word': word, 'uri': navigator.get_word_uri(word)} for word in meaning.related_words]
        }

    @staticmethod
    def serialize_multiple(meanings, navigator):
        return [MeaningSerializer.serialize(meaning, navigator) for meaning in meanings]
