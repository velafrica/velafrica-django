from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget

from velafrica.counter.models import Entry


class EntryResource(resources.ModelResource):
    """
    Define the resource for counter entry.
    """
    date = Field(
        column_name='date',
        attribute='date',
        widget=DateWidget(format="%d.%m.%Y"))

    class Meta:
        model = Entry
