from django import forms
from .models import InvoiceOrder, SbbTicketOrder, WalkthroughRequest, ContactRequest


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
    collected_before = forms.BooleanField(required=False, widget=forms.HiddenInput(attrs={
        'value': 'False'
    }))
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
    can_store = forms.BooleanField(required=False, widget=forms.HiddenInput(attrs={
        'value': 'False'
    }))
    can_deliver = forms.BooleanField(required=False, widget=forms.HiddenInput(attrs={
        'value': 'False'
    }))
    velafrica_pickup = forms.BooleanField(required=False, widget=forms.HiddenInput(attrs={
        'value': 'False'
    }))
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

    class Meta:
        model = WalkthroughRequest
        fields = (
            'first_name', 'last_name', 'phone', 'email', 'organizer_type', 'collected_before', 'collected_before_note',
            'date_fixed', 'date',
            'pickup_time_start', 'pickup_time_end', 'address', 'zip', 'address_note',
            'expected_velos', 'can_store', 'can_deliver', 'velafrica_pickup',
            'responsible_first_name', 'responsible_last_name', 'responsible_phone', 'responsible_email',
            'supporter_count', 'supporter_note'
        )


class SbbTicketOrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Vorname*'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Nachname*'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Strasse und Hausnummer*'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'PLZ und Ort*'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'email',
        'class': 'form-control input-lg',
        'placeholder': 'E-Mail*'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Telefonnumer*'
    }))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Bemerkung',
        'rows': '4'
    }))
    amount = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Menge an Velos'
    }))

    class Meta:
        model = SbbTicketOrder
        fields = ('first_name', 'last_name', 'amount', 'address', 'zip', 'email', 'phone', 'note')


class ContactRequestForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Vorname*'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Nachname*'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'E-Mail*'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Telefonnummer:'
    }))
    note = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Nachricht*'
    }))

    class Meta:
        model = ContactRequest
        fields = ('first_name', 'last_name', 'email', 'phone', 'note')
