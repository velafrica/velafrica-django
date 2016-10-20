from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import InvoiceForm


def order_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(form.cleaned_data['invoice_redirect_url'])

