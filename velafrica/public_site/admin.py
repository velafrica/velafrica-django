from django.contrib import admin
from .models import DonationAmount, InvoiceOrder, SbbTicketOrder, WalkthroughRequest, \
    Content, TeamMember, References, ContactRequest, Partner


class PartnerAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['country']


class ContentAdmin(admin.ModelAdmin):
    search_fields = ['path', 'key', 'description']
    list_filter = ['language', 'path']
    list_display = ['__unicode__', 'description']


class TeamMemberAdmin(admin.ModelAdmin):
    ordering = ('-sorting',)
    search_fields = ['name']


admin.site.register(Content, ContentAdmin)
admin.site.register(DonationAmount)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(References)
admin.site.register(InvoiceOrder)
admin.site.register(SbbTicketOrder)
admin.site.register(WalkthroughRequest)
admin.site.register(ContactRequest)
admin.site.register(Partner, PartnerAdmin)
