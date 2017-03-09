from django import forms
from .models import get_event_types_as_choice, TrackingStationQuery
from velafrica.sbbtracking.models import TrackingEventType


class TrackingStationQueryInlineAdminForm(forms.ModelForm):
    class Meta:
        model = TrackingStationQuery
        fields = ['label', 'event_types', 'query_order']

    def __init__(self, *args, **kwargs):
        super(TrackingStationQueryInlineAdminForm, self).__init__(*args, **kwargs)
        self.fields['event_types'] = forms.ModelMultipleChoiceField(
            queryset=TrackingEventType.objects.all(), widget=forms.CheckboxSelectMultiple
        )