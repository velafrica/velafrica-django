# -*- coding: utf-8 -*-
from rest_framework import generics, permissions

from velafrica.api.views import DjangoModelPermissionsMixin
from velafrica.collection.models import CollectionEvent
from velafrica.collection.serializer import CollectionEventPublicSerializer


class CollectionEventListPublic(DjangoModelPermissionsMixin, generics.ListAPIView):
    """
    Get a list of all Collection Events.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = CollectionEvent.objects.filter(public=True).order_by('date_start')
    serializer_class = CollectionEventPublicSerializer
    filter_fields = {'date_start': ['gte', 'lte'], 'date_end': ['gte', 'lte'], 'complete': ['exact']}
