from import_export import resources, fields

from velafrica.collection.models import TaskProgress, CollectionEvent, Dropoff


class TaskProgressResource(resources.ModelResource):
    """
    Define the collection event resource for import / export.
    """

    class Meta:
        model = TaskProgress
        fields = [
            'task',
            'task__name',
            'notes',
            'status',
            'collection_event',
            'collection_event__event__name',
        ]


class CollectionEventAdminResource(resources.ModelResource):
    """
    Define the collection event resource for import / export.
    """

    marketing_status = fields.Field()
    transport_status = fields.Field()
    feedback_status = fields.Field()

    def dehydrate_marketing_status(self, book):
        return book.get_status_marketing()

    def dehydrate_transport_status(self, book):
        return book.get_status_logistics()

    def dehydrate_feedback_status(self, book):
        return book.get_status_results()

    class Meta:
        model = CollectionEvent
        fields = [
            'date_start',
            'date_end',
            'event',
            'event__name',
            'event__region__name',
            'time',
            'notes',
            'presence_velafrica',
            'presence_velafrica_info',
            'collection',
            'collection_partner_vrn',
            'collection_partner_vrn__name',
            'collection_partner_other',
            'collection_partner_confirmed',
            'intermediate_store',
            'processing',
            'processing__name',
            'processing_notes',
            'website',
            'feedback',
            'velo_amount',
            'people_amount',
            'hours_amount',
            'additional_results',
            'event__description',
            'event__category__name',
            'event__yearly',
            'event__host',
            'event__host_type__name',
            'event__address__street',
            'event__address__city',
            'event__address__zipcode',
            'event__address_notes',
            'marketing_status',
            'transport_status',
            'feedback_status',
            'complete'
        ]


class DropoffResource(resources.ModelResource):
    """
    Define the Dropoff resource for import / export
    """

    class Meta:
        model = Dropoff
