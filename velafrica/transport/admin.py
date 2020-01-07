# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin, messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django_object_actions import DjangoObjectActions
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from import_export.widgets import DateWidget
from simple_history.admin import SimpleHistoryAdmin

from velafrica.organisation.models import Organisation
from velafrica.transport.filter import MultiListFilter
from velafrica.transport.forms import RideForm
from velafrica.transport.models import Car, Driver, VeloState, Ride, RequestCategory
from velafrica.transport.views import print_transport_request_view


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
            'customer_company', 'customer_salutation', 'customer_firstname', 'customer_lastname',
            'customer_email', 'customer_phone', 'customer_street_nr', 'customer_zip_code', 'customer_city',
            'invoice_same_as_customer', 'charged', 'price', 'invoice_company_name', 'invoice_company_addition',
            'invoice_street_nr', 'invoice_zip_code', 'invoice_city', 'invoice_commissioned', 'spare_parts', 'stocklist',
            'distance'
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
                        "success": "#4DFA90",  # green
                        "warning": "#FABE4D",  # orange
                        "danger": "#FF5468",  # red
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


class RideAdmin(ImportExportMixin, DjangoObjectActions, SimpleHistoryAdmin):
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
        'date',
        'date_created',
    ]

    readonly_fields = ['get_googlemaps_link', 'date_created', 'date_modified']
    changelist_actions = ['redirect_print_request_multiple', 'get_distances']
    change_actions = ['redirect_print_request_single', 'get_distance']
    actions = ['redirect_print_request_multiple', 'get_distances']

    fieldsets = (
        ('Transport', {
            'fields': (
                'date',
                ('driver', 'car'),
                'note',
                'velos',
                'completed'
            )
        }),
        (None, {
            'fields': (
                ('from_warehouse', 'to_warehouse'),
            )
        }),
        ('Auftrag', {
            'fields': (
                ('date_created', 'date_modified'),
                'created_by',
                'request_category',
                ('planned_velos', 'velo_state'),
                'request_comment'
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
            'classes': ('collapse',)
        }),
        ('Lieferadresse', {
            'fields': (
                'to_street_nr',
                'to_zip_code',
                'to_city',
                'to_contact_name',
            ),
            'classes': ('collapse',)
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
        ('Rechnung', {
            'fields': (
                'invoice_same_as_customer',
                'charged',
                'price',
                'invoice_company_name',
                'invoice_company_addition',
                'invoice_street_nr',
                'invoice_zip_code',
                'invoice_city',
                'invoice_commissioned'
            ),
            'classes': ('collapse',)
        }),
        ('Zusätzliche Infos', {
            'fields': (
                'spare_parts',
                'stocklist',
                'distance',
                'get_googlemaps_link'
            ),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        qs = super(RideAdmin, self).get_queryset(request)
        # superusers should see all entries
        if request.user.is_superuser:
            return qs
        # other users with a correlating person should only see their organisations entries
        elif hasattr(request.user, 'person'):
            return qs.filter(driver__organisation=request.user.person.organisation)
        # users with no superuser role and no related person should not see any entries
        else:
            return qs.none()

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
                   url(
                       r'^(?P<rides>.+)/print/$',  # comma separated pks of rides
                       view=print_transport_request_view,
                       name='print-request-view',
                   ),
               ] + super().get_urls()

    def print_transport_request_link(self, pks):
        return reverse(
            "admin:print-request-view",
            kwargs={
                "rides": ",".join(
                    str(pk) for pk in pks
                )
            }
        )

    def redirect_print_request_multiple(self, request, queryset):
        return HttpResponseRedirect(
            redirect_to=self.print_transport_request_link(
                pks=queryset.values_list('pk', flat=True)
            )
        )

    redirect_print_request_multiple.short_description = "Ausgewählte Aufträge drucken"

    def redirect_print_request_single(self, request, obj):
        return HttpResponseRedirect(
            redirect_to=self.print_transport_request_link(
                pks=[obj.pk]
            )
        )

    redirect_print_request_single.short_description = "Auftrag drucken"
    redirect_print_request_single.label = "Auftrag drucken"

    def print_request_button(self, obj):
        return format_html(
            u'<a href="{link}" title="{title}" target="_blank"><img src="{img}" /></a>',
            link=self.print_transport_request_link(pks=[obj.pk]),
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
            "screen": (static("css/ride-admin.css"),)
        }


admin.site.register(RequestCategory)
admin.site.register(Car, CarAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(VeloState, VeloStateAdmin)
admin.site.register(Ride, RideAdmin)
