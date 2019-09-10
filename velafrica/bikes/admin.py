# -*- coding: utf-8 -*-
import datetime
import io
import os

from django.conf.global_settings import MEDIA_ROOT
from django.conf.urls import url
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4

from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django.forms import model_to_dict
from django.utils.safestring import mark_safe
from django_object_actions import DjangoObjectActions
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from simple_history.admin import SimpleHistoryAdmin

from velafrica.bikes.models import Bike
from velafrica.core.settings import PROJECT_DIR

from reportlab.lib.utils import simpleSplit


class BikeResource(resources.ModelResource):
    class Meta:
        model = Bike


class APlusForSaleListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'A+ for sale'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'a_plus_for_sale'
    # boolean = True


    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('1', 'YES'),
            ('0', '-')
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '1':
            return queryset.filter(container__exact=None, a_plus__exact=True)


# TODO: show details fields as soon as A+ is selected
class BikeAdmin(ImportExportMixin, DjangoObjectActions, SimpleHistoryAdmin):
    labels = {key: Bike._meta.get_field(key).verbose_name for key in Bike.plotable}
    fontsize = 12
    line_height = 13

    resource_class = BikeResource  # import export

    list_display = ['number', 'type', 'brand', 'a_plus', 'for_sale', 'warehouse']
    search_fields = ['id', 'type', 'brand', 'a_plus', 'warehouse']
    list_filter = [APlusForSaleListFilter, 'a_plus', 'warehouse', 'type', ('date', DateRangeFilter), 'container']
    # change_actions = ('book_container',)
    # # inlines = [TrackingInline]

    def for_sale(self, obj):
        return obj.container is None

    # Set the column name in the change list

    for_sale.short_description = "For sale"
    # Set the field to use when ordering using this column
    for_sale.admin_order_field = 'container'

    for_sale.boolean = True

    actions = ["plot_to_pdf"]
    readonly_fields = ['id']

    fieldsets = (
        (None, {
            'fields': ('id', 'number', 'type', 'visa', 'date', 'warehouse')
        }),
        ('A+',  # Details ?
         {
             'fields': (
                 'a_plus',
                 'brand',
                 'bike_model',
                 'gearing',
#                 'crankset',
                 'drivetrain',
                 'type_of_brake',
                 'brake',
                 'colour',
                 'size',
                 'suspension',
                 'rear_suspension',
                 'extraordinary',
                 'image'
             ),
         }
         ),
        ('Container',
         {
             'fields': [
                 'container'
             ]
         }
         ),
    )

    # TODO: language-labels
    def draw_pdf_page(self, c, bike):
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        # W, H = landscape(A4)  # 841.9, 595.27

        # Header
        c.setFont("Helvetica", 32)
        c.drawString(x=40, y=510, text="A+ Bike")
        c.drawImage(
            os.path.join(PROJECT_DIR, 'frontend', 'static', 'img/velafrica_RGB.jpg'),
            x=657.5, y=471,
            width=2466 / 15, height=1565 / 15
        )

        # Bike
        c.setFont("Helvetica", self.fontsize)

        i = 0
        y = 450 - self.fontsize
        for key in Bike.plotable:
            if bike.__getattribute__(key):  # not blank
                c.drawString(40, y, self.labels[key])
                lines = simpleSplit(str(bike.__getattribute__(key)), c._fontname, c._fontsize, 130)
                for text in lines:
                    c.drawString(175, y, text)
                    y -= 14
                y -= 12


        if bike.image:
            w = 480  # fixed width
            h = bike.image.height / bike.image.width * w  # keep ratio
            c.drawImage(
                bike.image.url,
                x=321.9, y=450-h, width=w, height=h
            )

        c.showPage()  # New Page

    def plot_to_pdf(self, request, queryset):
        # Create a file-like buffer to receive PDF data.
        buf = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(
            buf,
            pagesize=landscape(A4)
        )

        for b in queryset:
            self.draw_pdf_page(p, b)

        # Close the PDF object cleanly, and we're done.
        p.save()
        buf.seek(0)

        response = StreamingHttpResponse(buf, content_type="application/pdf")
        response['Content-Disposition'] = "attachment;" + "filename={}_bikes.pdf".format(
            datetime.datetime.now().strftime('%Y-%m-%d'))

        return response


class BikeInline(admin.TabularInline):
    model = Bike
    fields = ('number', 'type', 'brand')
    extra = 0
    readonly_fields = []


admin.site.register(Bike, BikeAdmin)
