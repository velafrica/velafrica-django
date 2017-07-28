from velafrica.api.views import DjangoModelPermissionsMixin
from velafrica.organisation.models import Organisation
from velafrica.organisation.serializer import OrganisationSerializer
from rest_framework import generics


class OrganisationList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all organisations.
    TODO: filter
    """

    # queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer

    def get_queryset(self):
        qs = Organisation.objects.all()
        # superusers should see all entries
        if self.request.user.is_superuser:
            return qs
        # other users with a correlating person should only see their organisations entries
        elif hasattr(self.request.user, 'person'):
            return qs.filter(id=self.request.user.person.organisation.id)
        # users with no superuser role and no related person should not see any entries
        else:
            return qs.none()


class OrganisationDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of an organisation.
    """

    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
