from rest_framework import generics, permissions

from velafrica.api.views import DjangoModelPermissionsMixin
from velafrica.velafrica_sud.models import Container
from velafrica.velafrica_sud.serializer import ContainerSerializer


class ContainerList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all containers.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    filter_fields = ['organisation_from', 'partner_to', 'booked']
