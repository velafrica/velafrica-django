from django import forms
from .models import InvoiceOrder, SbbTicketOrder, WalkthroughRequest


class InvoiceForm(forms.ModelForm):
    invoice_redirect_url = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = InvoiceOrder
        fields = ('invoice_redirect_url', 'donation_amount', 'empty_invoice', 'number_invoices', 'first_name', 'last_name', 'address', 'zip', 'comment',)


class WalkthroughRequestForm(forms.ModelForm):
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Name*'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Vorname*'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Telefonnummer*'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'E-Mail*'
    }))
    organizer_type = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control input-lg'
    }), choices=WalkthroughRequest.PERSON_TYPE_CHOICES)
    collected_before = forms.BooleanField(required=False, widget=forms.HiddenInput)
    collected_before_note = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Wann und wo?',
        'rows': '4'
    }), required=False)
    date_fixed = forms.BooleanField(required=False, widget=forms.HiddenInput)
    date = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'date',
        'class': 'form-control input-lg',
        'placeholder': 'TT.MM.YYYY'
    }), required=False)

    pickup_time_start = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': '00:00',
    }))
    pickup_time_end = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': '00:00',
    }))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Strasse und Hausnummer',
    }))
    zip = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'PLZ und Ort',
    }))
    address_note = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Weiter Angaben zum Standort',
        'rows': '4',
    }))
    expected_velos = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'form-control input-lg',
        'placeholder': '',
    }), choices=WalkthroughRequest.EXPECTED_VELOS)
    can_store = forms.BooleanField(required=False, widget=forms.HiddenInput)
    can_deliver = forms.BooleanField(required=False, widget=forms.HiddenInput)
    velafrica_pickup = forms.BooleanField(required=False, widget=forms.HiddenInput)
    responsible_first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Name',
    }))
    responsible_last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Vorname',
    }))
    responsible_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Telefonnummer',
    }))
    responsible_email = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'E-Mail',
    }))
    supporter_count = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'form-control input-lg',
        'placeholder': '',
    }), choices=WalkthroughRequest.SUPPORTERS_COUNT)
    supporter_note = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Bemerkung',
        'rows': '4'
    }))


class SbbTicketOrderForm(forms.ModelForm):

    class Meta:
        model = SbbTicketOrder
        fields = ('first_name', 'last_name', 'address', 'zip', 'email', 'phone', 'note')
