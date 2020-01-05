from dal import autocomplete
from django import forms

from velafrica.bikes.models import Bike, BikeCategory
from velafrica.stock.models import Warehouse
from velafrica.velafrica_sud.models import Container


class BikeForm(forms.ModelForm):
    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:warehouse'),
        required=False,
        label='Warehouse'
    )
    container = forms.ModelChoiceField(
        queryset=Container.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:container'),
        required=False,
        label='Container'
    )
    category = forms.ModelChoiceField(
        queryset=BikeCategory.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:bike_category'),
        label='Category'
    )

    class Meta:
        model = Bike
        fields = ('__all__')
