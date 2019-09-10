# -*- coding: utf-8 -*-
import datetime
import io
import os

from django.conf.urls import url
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4

from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django_object_actions import DjangoObjectActions
from import_export import resources
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from velafrica.bikes.models import Bike
from velafrica.core.settings import PROJECT_DIR

from reportlab.lib.utils import simpleSplit


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
            return queryset.filter(container__exact=None, a_plus__exact=True)


# TODO: show details fields only when A+ is selected
class BikeAdmin(ImportExportMixin, DjangoObjectActions, SimpleHistoryAdmin):
    fontsize = 12  # pdf font size
    labels = {key: Bike._meta.get_field(key).verbose_name for key in Bike.plotable}  # labels for pdf

    resource_class = BikeResource  # import export

    list_display = ['number', 'type', 'brand', 'a_plus', 'for_sale', 'warehouse']
    search_fields = ['id', 'type', 'brand', 'a_plus', 'warehouse']
    list_filter = [APlusForSaleListFilter, 'a_plus', 'warehouse', 'type', ('date', DateRangeFilter), 'container']

    # "for_sale" a boolean column in the list-view
    def for_sale(self, obj):
        return obj.container is None

    for_sale.short_description = "For sale"
    for_sale.admin_order_field = 'container'
    for_sale.boolean = True

    # actions on selected elements
    actions = ["plot_to_pdf"]

    #
    #  Detail view
    #
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
                 # 'crankset',
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

    readonly_fields = ['id']

    # PDF-PLOT
    # TODO: language-labels
    def draw_pdf_page(self, c, bike):
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        # W, H = landscape(A4)  # 841.9, 595.27

        # Header : Title and Logo
        c.setFont("Helvetica", 32)
        c.drawString(x=40, y=510, text="A+ Bike")
        c.drawImage(
            os.path.join(PROJECT_DIR, 'frontend', 'static', 'img/velafrica_RGB.jpg'),
            x=657.5, y=471, width=2466 / 15, height=1565 / 15
        )

        # Bike
        c.setFont("Helvetica", self.fontsize)

        y = 450 - self.fontsize  # origin of coordinates is bottom left
        for key in Bike.plotable:
            if bike.__getattribute__(key):  # if not blank
                # label
                c.drawString(40, y, self.labels[key])

                # breaks lines if too long
                lines = simpleSplit(
                    text=str(bike.__getattribute__(key)),
                    fontName=c._fontname,
                    fontSize=c._fontsize,
                    maxWidth=130
                )

                # draw line by line
                for line in lines:
                    c.drawString(175, y, line)
                    y -= 14
                y -= 12  # add row spacing

        # plot image of bike
        if bike.image:
            w = 480  # fixed width
            h = bike.image.height / bike.image.width * w  # keep ratio
            c.drawImage(
                bike.image.url,
                x=321.9, y=450-h, width=w, height=h
            )

        # New Page
        c.showPage()

    def plot_to_pdf(self, request, queryset):
        # Create a file-like buffer to receive PDF data.
        buf = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(
            buf,
            pagesize=landscape(A4)
        )

        # create a pdf page for each bike
        for bike in queryset:
            self.draw_pdf_page(p, bike)

        # Close the PDF object cleanly
        p.save()
        buf.seek(0)

        # define HTT-Response
        response = StreamingHttpResponse(buf, content_type="application/pdf")  # set type to PDF
        # name the document and download it
        response['Content-Disposition'] = "attachment;filename={}_bikes.pdf".format(
            datetime.datetime.now().strftime('%Y-%m-%d')
        )
        return response


admin.site.register(Bike, BikeAdmin)
