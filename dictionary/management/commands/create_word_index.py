from django.core.management.base import BaseCommand, CommandError
from dictionary.factories import create_word_search_repo, create_word_repo

class Command(BaseCommand):
    help = 'Create word index on search engine'

    def handle(self, *args, **options):
        word_search_repo = create_word_search_repo()
        word_search_repo._create_word_index()

        self.stdout.write(self.style.SUCCESS('Successfully created word index'))
