# -*- coding: utf-8 -*-
from rest_framework import filters, permissions
from rest_framework import generics

from velafrica.counter.models import Entry
from velafrica.counter.serializer import EntrySerializer
from velafrica.api.views import DjangoModelPermissionsMixin

class CounterEntryList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all counter entries.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['organisation__id']

class CounterEntryDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get a detail view of a counter entry.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
