from dal import autocomplete
from django import forms

from velafrica.stock.models import Warehouse
from velafrica.transport.models import Ride, Driver, Car


class RideForm(forms.ModelForm):
    from_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:warehouse'),
        required=False,
        label='von'
    )
    to_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:warehouse'),
        required=False,
        label='nach'
    )
    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:driver'),
        required=False,
        label='Fahrer'
    )
    car = forms.ModelChoiceField(
        queryset=Car.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:car'),
        required=False,
        label='Fahrzeug'
    )

    class Meta:
        model = Ride
        fields = ('__all__')
