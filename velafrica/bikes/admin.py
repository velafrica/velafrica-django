# -*- coding: utf-8 -*-
import datetime
import io

from django.conf.global_settings import MEDIA_ROOT
from django.conf.urls import url
from django.http import FileResponse, HttpResponse
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


class BikeResource(resources.ModelResource):

    class Meta:
        model = Bike

# TODO: language-labels
def draw_pdf_page(c, bike):
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    # W, H = landscape(A4)  # 841.9, 595.27
    bikeD = model_to_dict(bike)

    l = [
        "number",
        "type",
        "brand",
        "gearing",
        "drivetrain",
        "type_of_brake",
        "brake",
        "colour",
        "size",
        "suspension",
        "extraordinary"
    ]

    # Header
    c.setFont("Helvetica", 32)
    c.drawString(x=50, y=510, text="A+ Bike")
    c.drawImage("velafrica/frontend/static/img/velafrica_RGB.jpg", x=657.5, y=471, width=2466/15, height=1565/15)

    # Bike
    fontsize = 12
    c.setFont("Helvetica", fontsize)

    i = 0
    for key in l:
        if bikeD[key]:
            c.drawString(50, 450 - 30*i - fontsize, key)
            c.drawString(160, 450 - 30 * i - fontsize, str(bikeD[key]))
            i += 1

    # Image
    if bike.image:
        w = 480
        h = bike.image.height / bike.image.width * w
        c.drawImage("velafrica/" + bike.image.url, 321.9, 450-h, width=w, height=h)

    # New Page
    c.showPage()


# TODO: show details fields as soon as A+ is selected
class BikeAdmin(ImportExportMixin, DjangoObjectActions, SimpleHistoryAdmin):
    resource_class = BikeResource  # import export

    list_display = ['number', 'type', 'brand', 'a_plus', 'container', 'warehouse']
    search_fields = ['number', 'type', 'brand', 'a_plus', 'container', 'warehouse']
    list_filter = ['type', ('date', DateRangeFilter), 'a_plus', 'container', 'warehouse']
    # change_actions = ('book_container',)
    # readonly_fields = ['container_n_of_all', 'container_n_of_year', 'time_to_customer']
    # # inlines = [TrackingInline]

    actions = ["plot_to_pdf"]

    fieldsets = (
        (None, {
            'fields': ('number', 'type', 'visum', 'date', 'warehouse')
            }),
        ('A+',
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

    def plot_to_pdf(self, request, queryset):
        # Create a file-like buffer to receive PDF data.
        buf = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(
            buf,
            pagesize=landscape(A4)
        )

        for b in queryset:
            draw_pdf_page(p, b)

        # Close the PDF object cleanly, and we're done.
        p.save()
        buf.seek(0)

        return HttpResponse(buf, content_type="application/pdf")

    plot_to_pdf.label = "Ausgewählte Velos als PDF drucken"

    #
    # def book_container(self, request, obj):
    #     """
    #     Admin action to book a container.
    #     """
    #     if obj:
    #         result = obj.book()
    #         print(result)
    #         if result:
    #             self.message_user(request, u"Container {} erfolgreich verbucht. {} von {} Trackings aktualisiert. ".format(obj.id, result[2], result[1]))
    #         else:
    #             self.message_user(request, "Container %s wurde bereits verbucht." % obj.id)
    #     else:
    #         self.message_user(request, "Not sure which Container to book." % obj.id)
    #
    # book_container.short_description = "Container Verbuchen"
    # book_container.label = "Verbuchen"


class BikeInline(admin.TabularInline):
    model = Bike
    fields = ('number', 'type', 'brand')
    extra = 0
    readonly_fields = []


admin.site.register(Bike, BikeAdmin)

