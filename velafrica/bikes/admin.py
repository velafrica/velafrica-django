# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import reverse, path
from import_export import resources
from import_export.admin import ImportExportMixin

from velafrica.bikes.forms import BikeForm
from velafrica.bikes.models import Bike, BikeCategory
from velafrica.bikes.views import book_bikes_view, BikePDFView
from velafrica.transport.filter import MultiListFilter


class BikeCategoryResource(resources.ModelResource):
    class Meta:
        model = BikeCategory


class BikeCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = BikeCategoryResource
    fields = ['name']


class BikeResource(resources.ModelResource):
    class Meta:
        model = Bike


class APlusFilter(MultiListFilter):
    title = 'A+'
    parameter_name = 'a_plus'

    def options(self):
        return [  # most return more than one
            MultiListFilter.Option(
                key='a_plus_sold',
                title='A+ sold',
                query=Q(
                    container__isnull=False,  # not yet sold and shipped within another container
                    a_plus__exact=True,  # is A+
                    status__exact=0  # status 'normal'
                )
            ),
            MultiListFilter.Option(
                key='a_plus_for_sale',
                title='A+ for sale',
                query=Q(
                    container__isnull=True,  # not yet sold and shipped within another container
                    a_plus__exact=True,  # is A+
                    status__exact=0  # status 'normal'
                )
            )
        ]


class BikeAdmin(ImportExportMixin, admin.ModelAdmin):
    form = BikeForm
    resource_class = BikeResource  # import export

    change_list_template = "bikes/change_list_bike.html"

    class Media:
        js = (
            static("js/bikes.js"),  # hides A+ fieldset
        )

    list_display = [
        'number',
        'category',
        'brand',
        'a_plus',
        'for_sale',
        'container',
        'warehouse',
    ]
    search_fields = [
        'brand',
        'number',
        'warehouse__name',
        'container__partner_to__organisation__name'
    ]
    list_filter = [
        APlusFilter,
        'category',
        'date',
        'container',
        'warehouse',
    ]

    # "for_sale" a boolean column in the list-view
    def for_sale(self, obj):
        return obj.container is None

    for_sale.short_description = "For sale"
    for_sale.admin_order_field = 'container'
    for_sale.boolean = True

    # actions on selected elements
    actions = ["plot_to_pdf", "book_bikes_action"]

    massadmin_exclude = [
        f.name for f in Bike._meta.get_fields()
        if f.name not in (
            'container',
            'warehouse',
            'a_plus',
        )
    ]

    #
    #  Detail view
    #

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'number',
                'category',
                ('date', 'visa'),
                'warehouse',
                'a_plus',
            )
        }),
        ('A+',  # A+ details
         {
             'fields': (
                 'brand',
                 'bike_model',
                 'gearing',
                 'drivetrain',
                 'brake',
                 'colour',
                 'size',
                 'suspension',
                 'rear_suspension',
                 'extraordinary',
                 'image'
             ),
             'classes': ('a_plus_fieldset',)
         }
         ),
        ('Container',
         {
             'fields': ('container',)
         }
         ),
    )

    readonly_fields = ['id']

    list_max_show_all = 1000
    list_per_page = 100

    def get_urls(self):
        return [
                   path(
                       'plot/<slug:key>/',
                       BikePDFView.as_view(),
                       name='bikes_plot'
                   )
               ] + super(BikeAdmin, self).get_urls()

    def plot_to_pdf(self, request, queryset):
        return redirect(
            reverse(
                "admin:bikes_plot",
                kwargs={
                    "pks": ",".join([str(q.pk) for q in queryset])
                }
            ),
        )

    plot_to_pdf.short_description = "Als PDF Drucken"



admin.site.register(Bike, BikeAdmin)
admin.site.register(BikeCategory, BikeCategoryAdmin)
