# -*- coding: utf-8 -*-
from rest_framework import filters, permissions
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from velafrica.api import utils
from velafrica.sbbtracking.serializer import *
from velafrica.stock.serializer import *
from velafrica.velafrica_sud.models import *
from velafrica.velafrica_sud.serializer import *


class DjangoModelPermissionsMixin(generics.GenericAPIView):
    """
    Permission Mixin
    """
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions,)


@api_view(('GET',))
def api_root(request, format=None):
    """
    This is the API of Velafrica (www.velafrica.ch)

    If you build something cool with it and want to show it to us, please do not hesitate!

    Send a link with description to nikolai.raeber (at) velafrica.ch

    Have fun!
    """

    response = utils.get_api_root_listing_from_urls(request, format)

    return Response(response)


class VeloTypeList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all velo types.
    """
    queryset = VeloType.objects.all()
    serializer_class = VeloTypeSerializer


class VeloTypeDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of a trackings.
    """

    queryset = VeloType.objects.all()
    serializer_class = VeloTypeSerializer

class TrackingList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all trackings.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ['tracking_no']


class TrackingDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of a trackings.
    """

    queryset = Tracking.objects.all()
    serializer_class = TrackingDetailSerializer


class TrackingEventList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all tracking events.
    """

    queryset = TrackingEvent.objects.all()
    serializer_class = TrackingEventSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ['tracking']


class TrackingEventDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of a trackings.
    """

    queryset = TrackingEvent.objects.all()
    serializer_class = TrackingEventSerializer


class TrackingEventTypeList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all trackings.
    """

    queryset = TrackingEventType.objects.all()
    serializer_class = TrackingEventTypeSerializer


class TrackingEventTypeDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of a trackings.
    """

    queryset = TrackingEventType.objects.all()
    serializer_class = TrackingEventTypeSerializer


class OrganisationList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all organisations.
    """

    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


class OrganisationDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of an organisation.
    """

    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


class WarehouseList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all warehouses.
    """

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of an warehouse.
    """

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class PartnerSudList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all African partners.
    """

    queryset = PartnerSud.objects.all()
    serializer_class = PartnerSudSerializer


class PartnerSudDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details about African partner.
    """

    queryset = PartnerSud.objects.all()
    serializer_class = PartnerSudSerializer

class ReportList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all partner Reports.
    """

    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details about on a specific partner report.
    """

    queryset = Report.objects.all()
    serializer_class = ReportSerializer