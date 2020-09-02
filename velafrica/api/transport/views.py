from rest_framework import generics

from velafrica.api.views import DjangoModelPermissionsMixin
from velafrica.transport.models import Ride
from velafrica.transport.serializer import RideSerializer


class RideList(DjangoModelPermissionsMixin, generics.ListAPIView):
    """
    Get a list of all rides.
    """

    queryset = Ride.objects.all()
    serializer_class = RideSerializer


class RideDetail(DjangoModelPermissionsMixin, generics.RetrieveAPIView):
    """
    Get details of a ride.
    """

    queryset = Ride.objects.all()
    serializer_class = RideSerializer
