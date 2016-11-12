from django.contrib import admin
from dictionary.models import Definition

class DefinitionAdmin(admin.ModelAdmin):
    list_display = ['word', 'meaning', 'extra', 'synonyms', 'related', 'origin', 'public'] 

admin.site.register(Definition, DefinitionAdmin)
