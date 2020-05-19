from django.core.management.base import BaseCommand, CommandError
from dictionary.factories import create_word_search_repo, create_word_repo

class Command(BaseCommand):
    help = 'Reindex all words on search engine'

    def handle(self, *args, **options):
        word_search_repo = create_word_search_repo()
        word_repo = create_word_repo()

        all_words_meanings = word_repo.get_all_words_meanings()
        for word_meaning in all_words_meanings:
            word_search_repo.index_word(word_meaning)

        self.stdout.write(self.style.SUCCESS('Successfully reindexed all words'))
