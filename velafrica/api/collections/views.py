# -*- coding: utf-8 -*-
from rest_framework import generics, permissions

from velafrica.api.views import DjangoModelPermissionsMixin
from velafrica.collection.models import CollectionEvent
from velafrica.collection.serializer import CollectionEventSerializer


class CollectionEventListPublic(DjangoModelPermissionsMixin, generics.ListAPIView):
    """
    Get a list of all Collection Events.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = CollectionEvent.objects.filter(public=True).order_by('date_start')
    serializer_class = CollectionEventSerializer
    filter_fields = ['date_start', 'date_end', 'complete']
    # filter_backends = (OrderingFilter,)
    # ordering_fields = '__all__'
    # ordering = ('date_start',)
