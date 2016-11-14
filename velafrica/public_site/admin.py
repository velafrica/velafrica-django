from django.contrib import admin
from .models import DonationAmount, InvoiceOrder, SbbTicketOrder, WalkthroughRequest

admin.site.register(InvoiceOrder)
admin.site.register(DonationAmount)
admin.site.register(SbbTicketOrder)
admin.site.register(WalkthroughRequest)
