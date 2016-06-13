from dal import autocomplete
from velafrica.organisation.models import Municipality
from velafrica.collection.models import Event
from django import forms


class EventForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(
        queryset=Municipality.objects.all(),
        widget=autocomplete.ModelSelect2(url='municipality-autocomplete')
    )

    class Meta:
        model = Event
        fields = ('__all__')