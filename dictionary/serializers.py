def serialize_meaning(meaning):
    return {
        'scientific': meaning.scientific,
        'type': meaning.type,
        'description': meaning.description,
        'extra_info': meaning.extra_info,
        'synonym_words': meaning.synonym_words,
        'related_words': meaning.related_words
    }

def serialize_word_meanings(word_meanings):
    return {'word': word_meanings.word,
            'meanings': [serialize_meaning(meaning) for meaning in word_meanings.meanings]}

def serialize_words_meanings(words_meanings):
    return [serialize_word_meanings(word_meanings) for word_meanings in words_meanings]
