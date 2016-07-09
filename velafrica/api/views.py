# -*- coding: utf-8 -*-
import markdown
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status, filters, permissions
from velafrica.organisation.models import *
from velafrica.organisation.serializer import *
from velafrica.sbbtracking.models import *
from velafrica.sbbtracking.serializer import *
from velafrica.stock.models import *
from velafrica.stock.serializer import *

class DjangoModelPermissionsMixin(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions,)


@api_view(('GET',))
def api_root(request, format=None):
    """
    This is the API of Velafrica (www.velafrica.ch)

    If you build something cool with it and want to show it to us, please do not hesitate!

    Send a link with description to nikolai.raeber (at) velafrica.ch

    Have fun!
    """

    queryset = Tracking.objects.none()

    from velafrica.api import urls
    from django.core.urlresolvers import RegexURLPattern, RegexURLResolver

    URL_NAMES = []
    def load_url_pattern_names(namespace, patterns):
        """Retrieve a list of urlpattern names"""
        URL_NAMES = []
        
        for pat in patterns:
            if pat.__class__.__name__ == 'RegexURLResolver':            # load patterns from this RegexURLResolver
                URL_NAMES.append(load_url_pattern_names(pat.namespace, pat.url_patterns))
            elif pat.__class__.__name__ == 'RegexURLPattern':           # load name from this RegexURLPattern
                # fully qualified pattern name :) (namespace::name)
                
                if pat.name is not None and pat.name not in URL_NAMES:
                    URL_NAMES.append((pat.name, pat.callback.__doc__))
        return (namespace, URL_NAMES)

    #root_urlconf = __import__(settings.ROOT_URLCONF)        # access the root urls.py file
    url_tree = load_url_pattern_names(None, urls.urlpatterns)   # access the "urlpatterns" from the ROOT_URLCONF

    response = {}
    for namespace_set in url_tree[1]:
        namespace = namespace_set[0]
        urls = namespace_set[1]
        namespace_urls = {}
        for ur in urls:
            if namespace:
                fqpn = '{}:{}'.format(namespace, ur[0])
                rev = ""
                try:
                    rev = reverse(str(fqpn), request=request, format=format)
                except:
                    try:
                        rev = reverse(str(fqpn), request=request, format=format, kwargs={'pk':1})
                    except:
                        print "something went wrong.. who cares :)"
                        pass
                    pass

                description = "{}".format(ur[1])
                namespace_urls[rev] = description.strip()
        response[namespace] = namespace_urls

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

