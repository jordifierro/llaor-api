def serialize_meaning(meaning):
    return {
        'scientific': meaning.scientific,
        'type': meaning.type,
        'description': meaning.description,
        'extra_info': meaning.extra_info,
        'synonym_words': meaning.synonym_words,
        'related_words': meaning.related_words
    }

def serialize_word(word):
    return {'word': word.word,
            'meanings': [serialize_meaning(meaning) for meaning in word.meanings]}

def serialize_words(words):
    return [serialize_word(word) for word in words]
