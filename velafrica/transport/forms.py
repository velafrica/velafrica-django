from dal import autocomplete
from django import forms

from velafrica.stock.models import Warehouse
from velafrica.transport.models import Ride, Driver, Car, VeloState, RequestCategory


class RideForm(forms.ModelForm):
    from_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:warehouse'),
        required=False,
        label='von (Standardadresse)',
        help_text='Nur für Standardadressen auswählen, sonst den Abschnittt "Abholadresse" verwenden.',
    )
    to_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:warehouse'),
        required=False,
        label='nach (Standardadresse)',
        help_text='Nur für Standardadressen auswählen, sonst den Abschnittt "Lieferadresse" verwenden.',
    )
    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:driver'),
        required=False,
        label='Fahrer'
    )
    co_driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:driver'),
        required=False,
        label='Beifahrer'
    )
    car = forms.ModelChoiceField(
        queryset=Car.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:car'),
        required=False,
        label='Fahrzeug'
    )
    velo_state = forms.ModelChoiceField(
        queryset=VeloState.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:velostate'),
        required=False,
        label="Transportgut"
    )
    request_category = forms.ModelChoiceField(
        queryset=RequestCategory.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:request_category'),
        required=False,
        label="Kategorie Velospender"
    )
    request_comment = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1}),
        required=False,
        label='Bemerkung',
        help_text="Bemerkung zum Auftrag"
    )

    note = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1}),
        required=False,
        label='Bemerkung',
        help_text="Bemerkung zur Fahrt"
    )

    class Meta:
        model = Ride
        fields = ('__all__')
