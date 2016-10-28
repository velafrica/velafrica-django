from django.contrib import admin
from .models import DonationAmount, InvoiceOrder

admin.site.register(InvoiceOrder)
admin.site.register(DonationAmount)
