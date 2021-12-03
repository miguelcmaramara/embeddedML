from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import HttpResponse
import json

from cloudant.client import Cloudant
import json

serviceUsername = "apikey-v2-2h972cxxcympef022f6sww9hl6h6zih6a1pwo9hsq05x"
servicePassword = "259fd79f304c8f861dc6bfb838a9a637"
serviceURL = "https://apikey-v2-2h972cxxcympef022f6sww9hl6h6zih6a1pwo9hsq05x:259fd79f304c8f861dc6bfb838a9a637@e89ade3e-f0d6-4d07-bcb2-3a771c849a68-bluemix.cloudantnosqldb.appdomain.cloud"

client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client.connect()

gestures = client['gestures']

if gestures.exists():
    print('success')


@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            data = json.loads(json.dumps(request.data, indent=4))
            gestures.create_document(data)
            response = HttpResponse(f"Submitted to database: {data}")
            return response
        except:
            response = HttpResponse(f"Error")
            return HttpResponse(status=400)


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """

    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            received_json_data = json.loads(request.body)
            print(received_json_data)
        except:
            pass
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
