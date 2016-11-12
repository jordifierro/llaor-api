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
        definition = Definition.objects.all()
        serializer = DefinitionSerializer(definition, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def definition_detail(request, key):
    """
    Retrieve definition
    """
    try:
        definition = Definition.objects.get(word=key)
    except Definition.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DefinitionSerializer(definition)
        return Response(serializer.data)
