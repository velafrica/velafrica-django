from django import forms
from .models import InvoiceOrder, SbbTicketOrder


class InvoiceForm(forms.ModelForm):
    invoice_redirect_url = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = InvoiceOrder
        fields = ('invoice_redirect_url', 'donation_amount', 'empty_invoice', 'number_invoices', 'first_name', 'last_name', 'address', 'zip', 'comment',)


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

    class Meta:
        model = SbbTicketOrder
        fields = ('first_name', 'last_name', 'address', 'zip', 'email', 'phone', 'note')
