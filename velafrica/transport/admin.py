# -*- coding: utf-8 -*-
from daterange_filter.filter import DateRangeFilter
from django.contrib import admin, messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse, path
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from import_export.widgets import DateWidget
from simple_history.admin import SimpleHistoryAdmin

from velafrica.organisation.models import Organisation
from velafrica.transport.filter import MultiListFilter
from velafrica.transport.forms import RideForm
from velafrica.transport.models import Car, Driver, VeloState, Ride, RequestCategory
from velafrica.transport.views import transport_request_pdf_view


class CarAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'organisation', 'plate']
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super(CarAdmin, self).get_queryset(request)
        # superusers should see all entries
        if request.user.is_superuser:
            return qs
        # other users with a correlating person should only see their organisations entries
        elif hasattr(request.user, 'person'):
            return qs.filter(organisation=request.user.person.organisation)
        # users with no superuser role and no related person should not see any entries
        else:
            return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organisation':
            if request.user.is_superuser:
                pass
            # other users with a correlating person should only see their organisation
            elif hasattr(request.user, 'person'):
                kwargs["queryset"] = Organisation.objects.filter(id=request.user.person.organisation.id)
            # users with no superuser role and no related person should not see any organisations
            else:
                kwargs["queryset"] = Organisation.objects.none()
        return super(CarAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class DriverAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'active', 'organisation']
    search_fields = ['name', 'organisation']
    list_filter = ['active']

    def get_queryset(self, request):
        qs = super(DriverAdmin, self).get_queryset(request)
        # superusers should see all entries
        if request.user.is_superuser:
            return qs
        # other users with a correlating person should only see their organisations entries
        elif hasattr(request.user, 'person'):
            return qs.filter(organisation=request.user.person.organisation)
        # users with no superuser role and no related person should not see any entries
        else:
            return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organisation':
            if request.user.is_superuser:
                pass
            # other users with a correlating person should only see their organisation
            elif hasattr(request.user, 'person'):
                kwargs["queryset"] = Organisation.objects.filter(id=request.user.person.organisation.id)
            # users with no superuser role and no related person should not see any organisations
            else:
                kwargs["queryset"] = Organisation.objects.none()
        return super(DriverAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class VeloStateAdmin(SimpleHistoryAdmin):
    list_display = ['name']
    search_fields = ['name']


class RideResource(resources.ModelResource):
    """
    Define the ride resource for import / export.
    """

    date = Field('date', 'date', DateWidget(format="%d.%m.%Y"))
    date_created = Field('date_created', 'date_created', DateWidget(format="%d.%m.%Y"))

    class Meta:
        model = Ride
        export_order = (
            'id', 'date_created', 'date', 'driver__name', 'car__name', 'velos', 'velo_state__name', 'note', 'completed',
            'from_warehouse__name', 'to_warehouse__name', 'created_by', 'request_category__category_name',
            'planned_velos', 'request_comment', 'from_street_nr', 'from_zip_code', 'from_city', 'from_contact_name',
            'from_contact_phone', 'from_comment', 'to_street_nr', 'to_zip_code', 'to_city', 'to_contact_name',
            'to_contact_phone', 'to_comment', 'customer_company', 'customer_salutation', 'customer_firstname',
            'customer_lastname', 'customer_email', 'customer_phone', 'customer_street_nr', 'customer_zip_code',
            'customer_city', 'invoice_same_as_customer', 'charged', 'invoice_purpose', 'price', 'cost_type',
            'invoice_company_name', 'invoice_company_addition', 'invoice_street_nr', 'invoice_zip_code', 'invoice_city',
            'invoice_commissioned', 'spare_parts', 'stocklist', 'distance', 'pickup_time',
        )
        fields = export_order


def get_status_circle(status, title=""):
    """
    Generates html for a colored circle
    """
    return format_html(
        '<div span style="{style}" title="{title}">&nbsp;</div>',
        style="; ".join(
            [
                "display: inline-block",
                "margin-right: 2px",
                "border-radius: 50%",
                "width: 20px",
                "height: 20px",
                "background-color: {color}".format(
                    color={
                        "success": "#20DD70",  # green
                        "warning": "#FABE4D",  # orange
                        "danger": "#FF5468",  # red

                        # more readable names
                        "completed": "#20DD70",  # green
                        "fixed": "#FFEE00",  # yellow
                        "printed": "#FABE4D",  # orange
                        "new": "#FF5468",  # red
                    }.get(status, "white")
                )
            ]
        ),
        title=title
    )


class TransportStatusFilter(MultiListFilter):
    title = 'Transportstatus'
    parameter_name = 'transport_status'

    def options(self):
        return [
            MultiListFilter.Option(
                key='new',
                title='Neue Aufträge',
                query=Q(completed__exact=False, date__isnull=True)
            ),
            MultiListFilter.Option(
                key='planned',
                title='Termin vereinbart',
                query=Q(completed__exact=False, date__isnull=False)
            ),
            MultiListFilter.Option(
                key='completed',
                title='Erledigte Aufträge',
                query=Q(completed__exact=True)
            )
        ]


class InvoiceStatusFilter(MultiListFilter):
    title = 'Rechnungsstatus'
    parameter_name = 'invoice_status'

    def options(self):
        return [
            MultiListFilter.Option(
                key='uncommissioned',
                title='Kostenpflichtige (noch nicht versendet)',
                query=Q(charged__exact=True, invoice_commissioned__exact=False)
            ),
            MultiListFilter.Option(
                key='commissioned',
                title='Rechnung versendet',
                query=Q(charged__exact=True, invoice_commissioned__exact=True)
            )
        ]


def single_transport_request_pdf(request, ride, **kwargs):
    return transport_request_pdf_view(
        request,
        rides=[get_object_or_404(Ride, pk=ride)],
        title="Transportauftrag {}".format(ride)
    )


class RideAdmin(ImportExportMixin, SimpleHistoryAdmin):
    form = RideForm
    resource_class = RideResource

    list_display = [
        'id',
        'print_request_button',
        'status',
        'date',
        'date_created',
        'start',
        'end',
    ]

    search_fields = [
        'id',
        'from_warehouse__name',
        'to_warehouse__name',
        'driver__name',
        'car__name'
    ]

    list_filter = [
        TransportStatusFilter,
        InvoiceStatusFilter,
        'request_category',
        ('date_created', DateRangeFilter),
        ('date', DateRangeFilter),
    ]

    readonly_fields = ['get_googlemaps_link', 'date_created', 'date_modified']
    change_actions = ['get_distance']
    actions = ['redirect_print_request_multiple', 'get_distances']

    fieldsets = (
        (None, {
            "fields": (
                ('velo_state', 'planned_velos',),
                'request_category',
                ('from_warehouse', 'to_warehouse'),
            ),
        }),

        ('Abholadresse', {
            'fields': (
                'from_street_nr',
                'from_zip_code',
                'from_city',
                'from_contact_name',
                'from_contact_phone',
                'from_comment'
            ),
            'classes': ('collapse', 'from_address',)
        }),
        ('Lieferadresse', {
            'fields': (
                'to_street_nr',
                'to_zip_code',
                'to_city',
                'to_contact_name',
                'to_contact_phone',
                'to_comment'
            ),
            'classes': ('collapse', 'to_address',)
        }),

        ('Auftraggeber*in', {
            'fields': (
                'customer_company',
                'customer_salutation',
                'customer_firstname',
                'customer_lastname',
                'customer_street_nr',
                'customer_zip_code',
                'customer_city',
                'customer_phone',
                'customer_email',
            ),
            'classes': ('collapse',)
        }),
        (None, {
            'fields': ('charged',)
        }),
        ('Rechnung', {
            'fields': (
                'invoice_same_as_customer',
                'invoice_purpose',
                'price',
                'cost_type',
                'invoice_company_name',
                'invoice_company_addition',
                'invoice_street_nr',
                'invoice_zip_code',
                'invoice_city',
                'invoice_commissioned'
            ),
            'classes': ('collapse', 'invoice')
        }),
        ('Auftrag', {
            'fields': (
                ('date_created', 'date_modified'),
                'created_by',
                'request_comment'
            ),
        }),
        ('Transport', {
            'fields': (
                ('date', 'pickup_time',),
                ('driver', 'car'),
                'note',
                'velos',
                'completed'
            )
        }),
        ('Zusätzliche Infos', {
            'fields': (
                'distance',
                'get_googlemaps_link'
            ),
            'classes': ('collapse',)
        })
    )

    def get_distance(self, request, obj):
        result = obj.get_distance()
        if type(result) == int:
            self.message_user(
                request,
                "Die Distanz zwischen {} und {} beträgt {} Meter.".format(
                    obj.get_from_address(),
                    obj.get_to_address(),
                    result
                )
            )
        else:
            self.message_user(
                request,
                "Die Distanz konnte nicht ermittelt werden.",
                level=messages.WARNING
            )

    get_distance.short_description = "Distanz berechnen"
    get_distance.label = "Distanz berechnen"

    def get_distances(self, request, queryset):
        count = 0
        for r in queryset:
            result = r.get_distance()
            if result:
                count += 1
        self.message_user(request, "Die Distanz wurde für {} Adressen gesetzt.".format(count))

    get_distances.short_description = "Distanz berechnen"

    def get_googlemaps_link(self, obj):
        maps_url = obj.get_googlemaps_url()
        return format_html(
            u"<a href='{}' target='_blank'>{}</a>",
            maps_url,
            "Auf Google Maps zeigen"
        ) if maps_url else ""

    get_googlemaps_link.short_description = 'Google Maps'

    def get_urls(self):
        return [
                   path(
                       'print/<int:ride>/',
                       view=single_transport_request_pdf,
                       name='print-request-view',
                   ),
               ] + super().get_urls()

    def redirect_print_request_multiple(self, request, queryset):
        return transport_request_pdf_view(request, rides=queryset, title="Transportaufträge")

    redirect_print_request_multiple.short_description = "Ausgewählte Aufträge drucken"

    def print_request_button(self, obj):
        return format_html(
            u'<a href="{link}" title="{title}"><img src="{img}" /></a>',
            link=reverse("admin:print-request-view", args=[obj.pk]),
            title='Drucken',
            img=static("img/print.png")
        )

    print_request_button.short_description = ""  # column header text is not needed

    def status(self, obj):
        status_html = get_status_circle(status=obj.get_status_ride(), title="Transportstatus")
        if obj.completed and obj.charged:
            status_html += get_status_circle(status=obj.get_status_invoice(), title="Rechnungsstatus")
        return status_html

    status.short_description = ""  # column header needed ?

    def start(self, obj):
        if obj.from_warehouse:
            return obj.from_warehouse
        return obj.get_from_address()

    start.short_description = "Start"

    def end(self, obj):
        if obj.to_warehouse:
            return obj.to_warehouse
        return obj.get_to_address()

    end.short_description = "Ziel"

    class Media:
        css = {
            "screen": ("css/ride-admin.css",),
        }
        js = ("js/ride-admin.js",)


admin.site.register(RequestCategory)
admin.site.register(Car, CarAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(VeloState, VeloStateAdmin)
admin.site.register(Ride, RideAdmin)
