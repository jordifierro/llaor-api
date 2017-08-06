from rest_framework import serializers
from dictionary.models import Definition


class DefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ('word', 'meaning', 'extra', 'synonyms', 'related', 'origin', 'semantic_group')
