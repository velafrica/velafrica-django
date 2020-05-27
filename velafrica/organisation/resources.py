from import_export import resources

from velafrica.organisation.models import Organisation


class OrganisationResource(resources.ModelResource):
    """
    Define the organisation resource for import / export.
    """

    class Meta:
        model = Organisation
