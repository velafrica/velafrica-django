# -*- coding: utf-8 -*-
from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_object_actions import DjangoObjectActions
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from simple_history.admin import SimpleHistoryAdmin

from velafrica.bikes.models import Bike
from velafrica.bikes.views import bikes_pdf
from velafrica.sbbtracking.models import Tracking
from velafrica.velafrica_sud.models import Forwarder, PartnerSud, Container, Report, ReportStaff, PartnerStaff, Role


class ReportInline(admin.TabularInline):
    """
    """
    model = Report
    extra = 0
    fields = ['creation']
    readonly_fields = ['creation']


class TrackingInline(admin.TabularInline):
    """
    """
    model = Tracking
    extra = 0
    can_delete = False
    editable_fields = []
    fields = ['tracking_no', 'first_name', 'last_name', 'email', 'last_event']

    def get_readonly_fields(self, request, obj=None):
        fields = []
        for field in self.model._meta.get_fields():
            if (not field == 'id'):
                if (field not in self.editable_fields):
                    fields.append(field)
        return fields
    
    def has_add_permission(self, request):
        return False

class ContainerResource(resources.ModelResource):
    """
    Define the Conainter resource for import / export.
    """

    class Meta:
        model = Container
        fields = ('container_no', 'container_n_of_year', 'organisation_from', 'organisation_from__name', 'partner_to', 'partner_to__organisation__name', 'velos_loaded', 'velos_unloaded', 'spare_parts', 'logistics', 'logistics__name', 'pickup_date', 'shipment_date', 'arrival_port_date', 'arrival_partner_date', 'velos_worth', 'spare_parts_worth', 'tools_worth', 'various_worth', 'seal_no', 'sgs_certified', 'notes')


class ContainerAdmin(ImportExportMixin, DjangoObjectActions, SimpleHistoryAdmin):
    resource_class = ContainerResource
    list_display = ['pickup_date', 'container_no', 'organisation_from', 'warehouse_from', 'partner_to', 'velos_loaded', 'velos_unloaded', 'spare_parts', 'booked', 'notes']
    search_fields = ['container_no', 'organisation_from__name', 'partner_to__organisation__name']
    list_filter = ['pickup_date', ('pickup_date', DateRangeFilter), 'organisation_from', 'partner_to',]
    change_actions = ('print_bikes', 'display_bikes', 'book_container',)
    readonly_fields = ['container_n_of_all', 'container_n_of_year', 'time_to_customer']
    #inlines = [TrackingInline]
    fieldsets = (
        (None, {
            'fields': ('container_no', 'warehouse_from', 'organisation_from', 'partner_to', 'velos_loaded', 'velos_unloaded', 'spare_parts', 'stocklist', 'booked')
            }),
        ('Transport', {
            'fields': ('logistics', 'pickup_date', 'arrival_port_date', 'arrival_partner_date', 'time_to_customer')
            }),
        ('Worth', {
            'fields': ('velos_worth', 'spare_parts_worth', 'tools_worth', 'various_worth'),
            'classes': ('collapse',)
            }),
        ('Extra info', {
            'fields': ('seal_no', 'sgs_certified', 'notes')
            })
    )

    def book_container(self, request, obj):
        """
        Admin action to book a container.
        """
        if obj:
            result = obj.book()
            print(result)
            if result:
                self.message_user(request, u"Container {} erfolgreich verbucht. {} von {} Trackings aktualisiert. ".format(obj.id, result[2], result[1]))
            else:
                self.message_user(request, "Container %s wurde bereits verbucht." % obj.id)
        else:
            self.message_user(request, "Not sure which Container to book." % obj.id)
        
    book_container.short_description = "Container Verbuchen"
    book_container.label = "Verbuchen"

    def print_bikes(self, request, obj):
        return bikes_pdf(
            request=request,
            queryset=Bike.objects.filter(container__exact=obj.id).order_by("number"),
            title='A+ bikes sold to {partner_name}'.format(
                partner_name=obj.partner_to.organisation.name
            ),
            subtitle="{:%d.%m.%Y}".format(obj.pickup_date),
            filename="{date:%y%m%d} A+ bikes sold to {partner_name}".format(
                date=obj.pickup_date,
                partner_name=obj.partner_to.organisation.name
            )
        )

    def display_bikes(self, request, obj):
        return redirect(
            reverse("admin:bikes_bike")
        )

    display_bikes.label = "Show bikes"

    print_bikes.label = format_html(
        "<img src='{img}' style='height: 16px; vertical-align:middle;' />&nbsp;{text}",
        img=static('img/print.png'),
        text="Bikes"
    )


class ContainerInline(admin.TabularInline):
    model = Container
    fields = ('pickup_date', 'container_no', 'organisation_from', 'velos_loaded', 'velos_unloaded', 'booked')
    extra = 0
    readonly_fields = ['booked']


class PartnerStaffInline(admin.TabularInline):
    """
    """
    model = PartnerStaff
    extra = 0


class PartnerSudAdmin(SimpleHistoryAdmin):
    list_display = ['organisation', 'get_googlemaps_link', 'get_container_count', 'get_bicycle_count']
    search_fields = ['organisation__name', 'organisation__address__country__name']
    readonly_fields = ['get_googlemaps_link', 'get_name', 'get_website', 'get_description', 'get_country', 'get_facebook', 'get_contact']
    inlines = [ContainerInline, PartnerStaffInline]
    fieldsets = (
        (None, {
            'fields': ('organisation', 'get_name', 'get_contact', 'get_website', 'get_facebook', 'get_description', 'image')
            }),
        ('Location', {
            'fields': ('get_googlemaps_link',)
            }),
        ('Organisation', {
            'fields': ('legalform', 'org_type', 'partner_since', 'vocational_training', 'infrastructure' )
            }),
    )

    def get_googlemaps_link(self, obj):
        a = obj.get_address()
        if a:
            url = a.get_googlemaps_url()
            if url:
                return mark_safe(u"<a href='{}' target='_blank'>{}</a>".format(
                    url,
                    a
                ))
            else:
                return ""
    get_googlemaps_link.short_description = 'Google Maps'

class ReportStaffInline(admin.TabularInline):
    """
    """
    model = ReportStaff
    extra = 0


class ReportResource(resources.ModelResource):
    """
    Define the Conainter resource for import / export.
    """
    economic_bicycles_turnover_USD = Field(readonly=True, attribute='economic_bicycles_turnover_USD', column_name='economic_bicycles_turnover_USD')
    economic_turnover_total_USD = Field(readonly=True, attribute='economic_turnover_total_USD', column_name='economic_turnover_total_USD')
    economic_spareparts_turnover_USD = Field(readonly=True, attribute='economic_spareparts_turnover_USD', column_name='economic_spareparts_turnover_USD')
    economic_services_turnover_USD = Field(readonly=True, attribute='economic_services_turnover_USD', column_name='economic_services_turnover_USD')
    economic_transport_costs_port_to_organisation_USD = Field(readonly=True, attribute='economic_transport_costs_port_to_organisation_USD', column_name='economic_transport_costs_port_to_organisation_USD')
    communityproject_reinvest_profit_total_USD = Field(readonly=True, attribute='communityproject_reinvest_profit_total_USD', column_name='communityproject_reinvest_profit_total_USD')

    class Meta:
        model = Report


class ReportAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = ReportResource
    list_display = ['creation', 'partner_sud']
    search_fields = ['partner_sud']
    list_filter = ['partner_sud', 'creation']
    inlines = [ReportStaffInline]
    readonly_fields = ['economic_bicycles_turnover_USD', 'economic_turnover_total_USD', 'economic_spareparts_turnover_USD', 'economic_services_turnover_USD', 'economic_transport_costs_port_to_organisation_USD', 'communityproject_reinvest_profit_total_USD']
    fieldsets = (
        (None, {
            'fields': ('creation', 'partner_sud', 'currency', 'currency_rate')
            }),
        ('Employment', {
            'classes': ('collapse', ),
            'fields': (
                'employment_fulltime_men', 
                'employment_fulltime_women', 
                'employment_parttime_men', 
                'employment_parttime_women', 
                'employment_volunteer_men', 
                'employment_volunteer_women', 
                'employment_internship_men',
                'employment_internship_women',
                'employment_trainee_men',
                'employment_trainee_women',
                'employment_notes',
                'employment_salary_calculation',
                )
            }),
        ('Economic', {
            'classes': ('collapse', ),
            'fields': (
                'economic_bicycles_amount',
                'economic_bicycles_turnover',
                'economic_bicycles_turnover_USD',
                'economic_spareparts_amount',
                'economic_spareparts_turnover',
                'economic_spareparts_turnover_USD',
                'economic_services_amount',
                'economic_services_turnover',
                'economic_services_turnover_USD',
                'economic_turnover_total',
                'economic_turnover_total_USD',
                'economic_import_taxes',
                'economic_transport_costs_port_to_organisation',
                'economic_transport_costs_port_to_organisation_USD',
                'economic_category1_name',
                'economic_category1_pricerange',
                'economic_category2_name',
                'economic_category2_pricerange',
                'economic_category3_name',
                'economic_category3_pricerange',
                'economic_category4_name',
                'economic_category4_pricerange',
                'economic_category5_name',
                'economic_category5_pricerange',
                'economic_category6_name',
                'economic_category6_pricerange',
                'economic_category7_name',
                'economic_category7_pricerange',
                'economic_category8_name',
                'economic_category8_pricerange',
                'economic_payment_types',
                'economic_notes'
                )
            }),
        ('Marketing Channels', {
            'classes': ('collapse', ),
            'fields': (
                'marketing_customer_segments',
                'marketing_customer_segments_other',
                'marketing_customer_segments_top1',
                'marketing_customer_segments_top2',
                'marketing_customer_segments_top3',
                'marketing_channels_mouth',
                'marketing_channels_radio',
                'marketing_channels_tv',
                'marketing_channels_socialmedia',
                'marketing_channels_poster',
                'marketing_channels_flyer',
                'marketing_channels_event_organisation',
                'marketing_channels_event_attendance',
                'marketing_channels_other',
                )
            }),
        ('Selling Channels', {
            'classes': ('collapse', ),
            'fields': (
                'marketing_sales_shop',
                'marketing_sales_outlets',
                'marketing_sales_retail',
                'marketing_sales_wholesale',
                'marketing_sales_other',
                )
            }),
        ('Vocational', {
            'classes': ('collapse', ),
            'fields': (
                'vocational_program_duration',
                'vocational_program_girls',
                'vocational_program_boys',
                'vocational_completed_girls',
                'vocational_completed_boys',
                'vocational_certificates',
                'vocational_certificates_ack',
                'vocational_exstudents_employed',
                'vocational_exstudents_selfemployed_new',
                'vocational_exstudents_selfemployed_link',
                'vocational_exstudents_bicycle_industry',
                'vocational_exstudents_agriculture',
                'vocational_exstudents_familiybusiness',
                'vocational_exstudents_energy',
                'vocational_notes'
                )
            }),
        ('Mobility', {
            'classes': ('collapse', ),
            'fields': (
                'mobilityprogram',
                'mobilityprogram_people_benefitted',
                'mobilityprogram_financial_support',
                'mobilityprogram_notes'
                )
            }),
        ('Community', {
            'classes': ('collapse', ),
            'fields': (
                'communityproject_reinvest_profit',
                'communityproject_areas',
                'communityproject_reinvest_profit_total',
                'communityproject_reinvest_profit_total_USD',
                'communityproject_people_benefitted',
                'communityproject_manager',
                'communityproject_notes'
                )
            }),
        ('Cooperation with Velafrica', {
            'classes': ('collapse', ),
            'fields': (
                'cooperation_quality_bicycles',
                'cooperation_quality_spares',
                'cooperation_quality_tools',
                'cooperation_ordering_experience',
                'cooperation_comments',
                )
            }),
        ('Final comments', {
            'classes': ('collapse', ),
            'fields': (
                'final_biggest_success',
                'final_future_challenges'
                )
            })

    )

admin.site.register(Container, ContainerAdmin)
admin.site.register(PartnerSud, PartnerSudAdmin)
admin.site.register(Forwarder)
admin.site.register(Role)
admin.site.register(Report, ReportAdmin)
