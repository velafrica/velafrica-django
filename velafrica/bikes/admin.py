# -*- coding: utf-8 -*-

from daterange_filter.filter import DateRangeFilter
from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import reverse, path
from django_object_actions import DjangoObjectActions
from import_export import resources
from import_export.admin import ImportExportMixin

from velafrica.bikes.forms import BikeForm
from velafrica.bikes.models import Bike, BikeCategory
from velafrica.bikes.views import book_bikes_view, BikePDFView


class BikeCategoryResource(resources.ModelResource):
    class Meta:
        model = BikeCategory


class BikeCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = BikeCategoryResource
    fields = ['name']


class BikeResource(resources.ModelResource):
    class Meta:
        model = Bike


# Filters out all A+ Bikes which are still for sale
class APlusForSaleListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'A+ for sale'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'a_plus_for_sale'

    def lookups(self, request, model_admin):
        return (  # most return more than one
            ('1', 'YES'),
            ('0', '-')
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(
                container__exact=None,  # not yet sold and shipped within another container
                a_plus__exact=True,  # is A+
                status__exact=0  # status 'normal'
            )


# TODO: show details fields only when A+ is selected
class BikeAdmin(ImportExportMixin, DjangoObjectActions, admin.ModelAdmin):
    form = BikeForm

    class Media:
        js = (
            static("js/bikes.js"),  # hides A+ fieldset
        )

    resource_class = BikeResource  # import export

    list_display = ['number', 'category', 'brand', 'a_plus', 'for_sale', 'container', 'warehouse']
    search_fields = ['id', 'category', 'brand', 'a_plus', 'warehouse']
    list_filter = [APlusForSaleListFilter, 'a_plus', 'category', 'container', 'warehouse', ('date', DateRangeFilter)]

    # "for_sale" a boolean column in the list-view
    def for_sale(self, obj):
        return obj.container is None

    for_sale.short_description = "For sale"
    for_sale.admin_order_field = 'container'
    for_sale.boolean = True

    # actions on selected elements
    actions = ["plot_to_pdf", "book_bikes_action"]

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
        ('A+',  # Details ?
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
             'fields': ['container']
         }
         ),
    )

    readonly_fields = ['id']

    list_max_show_all = 1000
    list_per_page = 100

    def get_urls(self):
        return [
                   url(
                       r'^book/(?P<object_ids>[\w,\.\-]+)/$',
                       self.book_bikes,
                       name='bikes_bike_book'
                   ),
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

    def book_bikes(self, *args, **kwargs):
        return book_bikes_view(self, *args, **kwargs)

    def book_bikes_action(self, request, queryset):
        return HttpResponseRedirect(
            add_preserved_filters(
                context={
                    'preserved_filters': self.get_preserved_filters(request),
                    'opts': queryset.model._meta
                },
                url=reverse(
                    "admin:bikes_bike_book",
                    kwargs={
                        "object_ids": ",".join(
                            str(q.pk)
                            for q in queryset
                        )
                    }
                )
            )
        )

    book_bikes_action.short_description = "Velos buchen / verschieben"


admin.site.register(Bike, BikeAdmin)
admin.site.register(BikeCategory, BikeCategoryAdmin)
