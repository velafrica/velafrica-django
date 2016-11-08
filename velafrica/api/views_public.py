# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models import Q
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from velafrica.collection.models import Dropoff
from velafrica.collection.serializer import DropoffSerializer

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_dropoffs(request):
    q = Q(temp=True) & Q(temp_end__lt=datetime.now().date().strftime('%Y-%m-%d'))
    all = Dropoff.objects.filter(active=True).exclude(q)

    serializer = DropoffSerializer(all, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny,))
def subscribe_newsletter(request):
    pass
