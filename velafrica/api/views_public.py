# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from velafrica.collection.models import Dropoff
from velafrica.collection.serializer import DropoffSerializer

@api_view(['GET'])
# @renderer_classes((JSONRenderer,))
@permission_classes((AllowAny,))
def get_dropoffs(request):
    dropoffs = Dropoff.objects.filter(active=True)
    serializer = DropoffSerializer(dropoffs, many=True)
    return Response(serializer.data)
