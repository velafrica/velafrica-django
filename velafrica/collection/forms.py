from dal import autocomplete
from velafrica.organisation.models import Municipality
from velafrica.collection.models import CollectionEvent
from django import forms


class CollectionEventForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(
        queryset=Municipality.objects.all(),
        widget=autocomplete.ModelSelect2(url='municipality-autocomplete')
    )

    class Meta:
        model = CollectionEvent
        fields = ('__all__')