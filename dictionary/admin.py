from django.contrib import admin
from dictionary.models import Definition


class DefinitionAdmin(admin.ModelAdmin):
    list_display = ['word', 'phonetic', 'scientific', 'type', 'meaning', 'extra_info', 'private_notes',
                    'synonyms', 'related', 'semantic_field', 'origin', 'reviewed', 'public']
    search_fields = ['word', 'scientific', 'meaning', 'extra_info', 'private_notes',
                     'synonyms', 'related', 'semantic_field', 'origin', 'source']
    list_filter = ['reviewed', 'public', 'source', 'semantic_field', 'origin', 'type']


admin.site.register(Definition, DefinitionAdmin)
