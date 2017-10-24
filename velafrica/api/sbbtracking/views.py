from velafrica.api.views import DjangoModelPermissionsMixin
from velafrica.sbbtracking.models import Tracking, TrackingEvent
from velafrica.sbbtracking.serializer import TrackingSerializer, TrackingEventSerializer
from rest_framework import generics, permissions

class TrackingList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all trackings.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer
    filter_fields = ['tracking_no']


class TrackingEventList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all tracking events.
    """

    queryset = TrackingEvent.objects.all()
    serializer_class = TrackingEventSerializer
    filter_fields = ['tracking']