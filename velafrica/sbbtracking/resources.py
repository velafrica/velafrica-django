from import_export import resources

from velafrica.sbbtracking.models import Tracking


class TrackingResource(resources.ModelResource):
    """
    Define the Tracking resource for import / export.
    """

    class Meta:
        model = Tracking
        import_id_fields = ('tracking_no',)
        fields = ('first_name', 'last_name', 'email', 'tracking_no', 'last_event__event_type__name', 'velo_type__name')
