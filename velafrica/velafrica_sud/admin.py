# -*- coding: utf-8 -*-
from daterange_filter.filter import DateRangeFilter
from django_object_actions import DjangoObjectActions
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from velafrica.sbbtracking.models import Tracking
from velafrica.velafrica_sud.models import Country, Forwarder, PartnerSud, Container, Report, Staff, Role
from import_export import resources
from import_export.admin import ImportExportMixin
from django.shortcuts import render_to_response

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
        for field in self.model._meta.get_all_field_names():
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
        fields = ('container_no', 'organisation_from', 'organisation_from__name', 'partner_to', 'partner_to__name', 'velos_loaded', 'velos_unloaded', 'spare_parts', 'logistics', 'logistics__name', 'pickup_date', 'shipment_date', 'arrival_port_date', 'arrival_partner_date', 'velos_worth', 'spare_parts_worth', 'tools_worth', 'various_worth', 'seal_no', 'sgs_certified', 'notes')


class ContainerAdmin(ImportExportMixin, DjangoObjectActions, SimpleHistoryAdmin):
    resource_class = ContainerResource
    list_display = ['pickup_date', 'container_n_of_all', 'container_no', 'organisation_from', 'warehouse_from', 'partner_to', 'velos_loaded', 'velos_unloaded', 'spare_parts', 'booked', 'notes']
    search_fields = ['container_no', 'organisation_from__name', 'partner_to__name']
    list_filter = ['pickup_date', ('pickup_date', DateRangeFilter), 'organisation_from', 'partner_to',]
    change_actions = ('book_container',)
    readonly_fields = ['container_n_of_all']
    inlines = [TrackingInline]
    fieldsets = (
        (None, {
            'fields': ('container_n_of_all', 'container_no', 'warehouse_from', 'organisation_from', 'partner_to', 'velos_loaded', 'velos_unloaded', 'spare_parts', 'stocklist', 'booked')
            }),
        ('Transport', {
            'fields': ('logistics', 'pickup_date', 'shipment_date', 'arrival_port_date', 'arrival_partner_date')
            }),
        ('Worth', {
            'fields': ('velos_worth', 'spare_parts_worth', 'tools_worth', 'various_worth')
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
            print result
            if result:
                self.message_user(request, u"Container {} erfolgreich verbucht. {} von {} Trackings aktualisiert. ".format(obj.id, result[2], result[1]))
            else:
                self.message_user(request, "Container %s wurde bereits verbucht." % obj.id)
        else:
            self.message_user(request, "Not sure which Container to book." % obj.id)
        
    book_container.short_description = "Container Verbuchen"
    book_container.label = "Verbuchen"


class ContainerInline(admin.TabularInline):
    model = Container
    fields = ('pickup_date', 'container_no', 'organisation_from', 'velos_loaded', 'velos_unloaded', 'booked')
    extra = 0
    readonly_fields = ['booked']

class PartnerSudAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'country', 'website', 'get_container_count', 'get_bicycle_count']
    search_fields = ['name', 'country__name']
    readonly_fields = ['name', 'description', 'website', 'contact', 'street', 'zipcode', 'area', 'country', 'longitude', 'latitude']
    inlines = [ContainerInline, ]
    fieldsets = (
        (None, {
            'fields': ('organisation', 'name', 'description', 'website', 'image', 'contact' )
            }),
        ('Location', {
            'fields': ('street', 'zipcode', 'area', 'country', 'longitude', 'latitude')
            }),
        ('Organisation', {
            'fields': ('legalform', 'org_type', 'partner_since', 'vocational_training', 'infrastructure' )
            }),
    )


class StaffInline(admin.TabularInline):
    """
    """
    model = Staff
    extra = 0


class ReportResource(resources.ModelResource):
    """
    Define the Conainter resource for import / export.
    """

    class Meta:
        model = Report


class ReportAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = ReportResource
    list_display = ['creation', 'partner_sud']
    search_fields = ['partner_sud']
    list_filter = ['partner_sud', 'creation']
    inlines = [StaffInline]
    fieldsets = (
        (None, {
            'fields': ('creation', 'partner_sud')
            }),
        ('Employment', {
            'classes': ('collapse', ),
            'fields': (
                'employment_salary_calculation',
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
                )
            }),
        ('Economic', {
            'classes': ('collapse', ),
            'fields': (
                'economic_bicycles_amount',
                'economic_bicycles_turnover',
                'economic_spareparts_amount',
                'economic_spareparts_turnover',
                'economic_services_amount',
                'economic_services_turnover',
                'economic_turnover_total',
                'economic_import_taxes',
                'economic_transport_costs_port_to_organisation',
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
admin.site.register(Country)
admin.site.register(Forwarder)
admin.site.register(Role)
admin.site.register(Report, ReportAdmin)
