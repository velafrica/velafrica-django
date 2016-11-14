from django.contrib import admin
from .models import DonationAmount, InvoiceOrder, SbbTicketOrder

admin.site.register(InvoiceOrder)
admin.site.register(DonationAmount)
admin.site.register(SbbTicketOrder)
