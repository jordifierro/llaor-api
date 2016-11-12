from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dictionary.models import Definition
from dictionary.serializers import DefinitionSerializer

@api_view(['GET'])
def dictionary_list(request):
    """
    List all definitions
    """
    if request.method == 'GET':
        definitions = Definition.objects.all()
        serializer = DefinitionSerializer(definitions, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def definition_detail(request, key):
    """
    Retrieve definition
    """
    definitions = Definition.objects.filter(word=key)
    if len(definitions) == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DefinitionSerializer(definitions, many=True)
        return Response(serializer.data)
