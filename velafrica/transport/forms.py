from dal import autocomplete
from django import forms

from velafrica.stock.models import Warehouse
from velafrica.transport.models import Ride


class RideForm(forms.ModelForm):
    from_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:warehouse')
    )
    to_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:warehouse')
    )

    class Meta:
        model = Ride
        fields = ('__all__')
