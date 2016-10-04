# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from velafrica.collection.models import CollectionEvent
from velafrica.collection.serializer import CollectionEventSerializer

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
@permission_classes((AllowAny,))
def get_collection(request):
    collection_events = CollectionEvent.objects.all()
    serializer = CollectionEventSerializer(collection_events, many=True)
    return Response(serializer.data)
