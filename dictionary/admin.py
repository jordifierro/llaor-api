from django.contrib import admin
from dictionary.models import Definition

class DefinitionAdmin(admin.ModelAdmin):
    list_display = ['word', 'phonetic', 'meaning', 'extra_info',
                    'private_notes', 'synonyms', 'related', 'origin', 'reviewed', 'public'] 
    search_fields = ['word', 'meaning', 'extra_info', 'private_notes',
                     'synonyms', 'related', 'origin', 'source']
    list_filter = ['reviewed', 'public', 'source', 'origin']

admin.site.register(Definition, DefinitionAdmin)
