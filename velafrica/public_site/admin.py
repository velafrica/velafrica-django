from django.contrib import admin
from .models import DonationAmount, InvoiceOrder, SbbTicketOrder, WalkthroughRequest, \
    Content, TeamMember, Award, ContactRequest

class ContentAdmin(admin.ModelAdmin):
    search_fields = ['path', 'key', 'description']
    list_filter = ['language', 'path']
    list_display = ['__unicode__', 'description']


admin.site.register(Content, ContentAdmin)
admin.site.register(DonationAmount)
admin.site.register(TeamMember)
admin.site.register(Award)
admin.site.register(InvoiceOrder)
admin.site.register(SbbTicketOrder)
admin.site.register(WalkthroughRequest)
admin.site.register(ContactRequest)
