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


class BikeResource(resources.ModelResource):
    class Meta:
        model = Bike


# TODO: show details fields as soon as A+ is selected
class BikeAdmin(ImportExportMixin, DjangoObjectActions, SimpleHistoryAdmin):
    labels = {key: Bike._meta.get_field(key).verbose_name for key in Bike.plotable}
    fontsize = 12

    resource_class = BikeResource  # import export

    list_display = ['id', 'type', 'brand', 'a_plus', 'for_sale', 'warehouse']
    search_fields = ['id', 'type', 'brand', 'a_plus', 'for_sale', 'warehouse']
    list_filter = ['for_sale', 'a_plus', 'warehouse', 'type', ('date', DateRangeFilter)]
    # change_actions = ('book_container',)
    # # inlines = [TrackingInline]

    def for_sale(self, obj):
        return obj.container is None

    actions = ["plot_to_pdf"]
    readonly_fields = ['id']

    fieldsets = (
        (None, {
            'fields': ('id', 'number', 'type', 'visum', 'date', 'warehouse')
        }),
        ('A+',  # Details ?
         {
             'fields': (
                 'a_plus',
                 'brand',
                 'gearing',
                 'drivetrain',
                 'type_of_brake',
                 'brake',
                 'colour',
                 'size',
                 'suspension',
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
        c.drawString(x=50, y=510, text="A+ Bike")
        c.drawImage(
            os.path.join(PROJECT_DIR, 'frontend', 'static', 'img/velafrica_RGB.jpg'),
            x=657.5, y=471,
            width=2466 / 15, height=1565 / 15
        )

        # Bike
        c.setFont("Helvetica", self.fontsize)

        i = 0
        for key in Bike.plotable:
            if bike.__getattribute__(key):  # not blank
                c.drawString(50, 450 - 30 * i - self.fontsize, self.labels[key])
                c.drawString(160, 450 - 30 * i - self.fontsize, str(bike.__getattribute__(key)))
                i += 1

        if bike.image:
            w = 480
            h = bike.image.height / bike.image.width * w
            c.drawImage(bike.image.url, 321.9, 450 - h, width=w, height=h)

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
