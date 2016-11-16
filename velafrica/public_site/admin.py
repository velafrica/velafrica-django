from django.contrib import admin
from .models import DonationAmount, InvoiceOrder, SbbTicketOrder, WalkthroughRequest, Content

class ContentAdmin(admin.ModelAdmin):
    search_fields = ['path', 'key', 'description']
    list_filter = ['language', 'path']
    list_display = ['__unicode__', 'description']


admin.site.register(InvoiceOrder)
admin.site.register(DonationAmount)
admin.site.register(SbbTicketOrder)
admin.site.register(WalkthroughRequest)
admin.site.register(Content, ContentAdmin)
