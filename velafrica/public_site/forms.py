from django import forms
from .models import InvoiceOrder, WalkthroughRequest


class InvoiceForm(forms.ModelForm):
    invoice_redirect_url = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = InvoiceOrder
        fields = ('invoice_redirect_url', 'donation_amount', 'empty_invoice', 'number_invoices', 'first_name', 'last_name', 'address', 'zip', 'comment',)


class WalkthroughRequestForm(forms.ModelForm):

    class Meta:
        model = WalkthroughRequest
        fields = (
            'first_name', 'last_name', 'phone', 'email', 'organizer_type', 'organizer_type_note',
            'date_start', 'date_end', 'pickup_time_start', 'pickup_time_end', 'address', 'zip', 'address_note',
            'expected_velos', 'can_store', 'can_deliver', 'velafrica_pickup',
            'responsible_first_name', 'responsible_last_name', 'responsible_phone', 'responsible_email',
            'supporter_count', 'supporter_note'
        )
