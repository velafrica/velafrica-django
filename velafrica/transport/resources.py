from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget

from velafrica.transport.models import Ride


class RideResource(resources.ModelResource):
    """
    Define the ride resource for import / export.
    """

    date = Field('date', 'date', DateWidget(format="%d.%m.%Y"))
    date_created = Field('date_created', 'date_created', DateWidget(format="%d.%m.%Y"))

    class Meta:
        model = Ride
        export_order = (
            'id', 'date_created', 'date', 'driver__name', 'car__name', 'velos', 'velo_state__name', 'note', 'completed',
            'from_warehouse__name', 'to_warehouse__name', 'created_by', 'request_category__category_name',
            'planned_velos', 'request_comment', 'from_street_nr', 'from_zip_code', 'from_city', 'from_contact_name',
            'from_contact_phone', 'from_comment', 'to_street_nr', 'to_zip_code', 'to_city', 'to_contact_name',
            'to_contact_phone', 'to_comment', 'customer_company', 'customer_salutation', 'customer_firstname',
            'customer_lastname', 'customer_email', 'customer_phone', 'customer_street_nr', 'customer_zip_code',
            'customer_city', 'invoice_same_as_customer', 'charged', 'invoice_purpose', 'price', 'cost_type',
            'invoice_company_name', 'invoice_company_addition', 'invoice_street_nr', 'invoice_zip_code', 'invoice_city',
            'invoice_commissioned', 'spare_parts', 'stocklist', 'distance', 'pickup_time',
        )
        fields = export_order
