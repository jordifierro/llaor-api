from django.contrib import admin
from dictionary.models import Definition

class DefinitionAdmin(admin.ModelAdmin):
    list_display = ['word', 'meaning', 'extra', 'synonyms', 'related', 'origin', 'public'] 
    search_fields = ['word', 'meaning', 'extra', 'origin', 'synonyms', 'related', 'source']
    list_filter = ['public', 'source', 'origin']

admin.site.register(Definition, DefinitionAdmin)
