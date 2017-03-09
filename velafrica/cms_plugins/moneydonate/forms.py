from django import forms
from .models import InvoiceOrder


class InvoiceForm(forms.ModelForm):
    invoice_redirect_url = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = InvoiceOrder
        fields = ['invoice_redirect_url', 'donation_amount', 'empty_invoice', 'number_invoices', 'first_name', 'last_name', 'address', 'zip', 'comment']
