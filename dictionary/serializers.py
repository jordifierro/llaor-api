class MeaningSerializer(object):

    @staticmethod
    def serialize(meaning):
        return {
            'scientific': meaning.scientific,
            'type': meaning.type,
            'description': meaning.description,
            'extra_info': meaning.extra_info,
            'synonym_words': [{'word': word} for word in meaning.synonym_words],
            'related_words': [{'word': word} for word in meaning.related_words]
        }

    @staticmethod
    def serialize_multiple(word, meanings):
        return {'word': word,
                'meanings': [MeaningSerializer.serialize(meaning) for meaning in meanings]}
