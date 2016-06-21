from dal import autocomplete
from velafrica.stock.models import Warehouse
from velafrica.transport.models import Ride
from velafrica.collection.models import Event
from django import forms


class RideForm(forms.ModelForm):
    from_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=autocomplete.ModelSelect2(url='warehouse-autocomplete')
    )
    to_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=autocomplete.ModelSelect2(url='warehouse-autocomplete')
    )

    class Meta:
        model = Ride
        fields = ('__all__')
