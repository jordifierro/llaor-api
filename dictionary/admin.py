from django.contrib import admin
from dictionary.models import Definition


class DefinitionAdmin(admin.ModelAdmin):
    list_display = ['word', 'phonetic', 'scientific', 'type', 'meaning', 'extra_info',
                    'private_notes', 'synonyms', 'related', 'origin', 'reviewed', 'public']
    search_fields = ['word', 'scientific', 'meaning', 'extra_info', 'private_notes',
                     'synonyms', 'related', 'origin', 'source']
    list_filter = ['reviewed', 'public', 'source', 'origin', 'type']


admin.site.register(Definition, DefinitionAdmin)
