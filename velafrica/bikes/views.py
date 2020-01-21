# -*- coding: utf-8 -*-
import datetime
import io
import os

from dal import autocomplete
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.views import View
from django.views.generic import ListView
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

from velafrica.bikes.models import Bike, BikeCategory
from velafrica.core.settings import PROJECT_DIR
from velafrica.velafrica_sud.models import Container


class BikePDFView(View):
    fontsize = 12  # pdf font size

    # fields used from plot_to_pdf
    fields = {
        "number": "No.",
        "category": "Type",
        "brand": "Brand",
        "bike_model": "Model",
        "gearing": "Group of components",
        "drivetrain": "Drivetrain",
        "brake": "Brake",
        "colour": "Colour",
        "size": "Size",
        "suspension": "Suspension",
        "rear_suspension": "Rear suspension"
    }

    # PDF-PLOT
    # TODO: language-labels
    def draw_pdf_page(self, c, bike):
        # Header - Title and Logo
        c.setFont("Helvetica", 32)
        c.drawString(x=40, y=510, text="A+ Bike")
        c.drawImage(
            os.path.join(PROJECT_DIR, 'frontend', 'static', 'img/velafrica_RGB.jpg'),
            x=657.5, y=471, width=2466 / 15, height=1565 / 15
        )

        # Bike
        c.setFont("Helvetica", self.fontsize)

        y = 450 - self.fontsize  # origin of coordinates is bottom left
        for key, label in self.fields.items():
            if bike.__getattribute__(key):  # if not blank
                # label
                c.drawString(40, y, label)

                # breaks lines if too long
                # and then draw line by line
                for line in simpleSplit(text=str(bike.__getattribute__(key)),
                                        fontName=c._fontname,
                                        fontSize=c._fontsize,
                                        maxWidth=130):
                    c.drawString(175, y, line)
                    y -= 15
                # add spacing between two rows
                y -= 6

        if bike.extraordinary and bike.extraordinary != "":
            c.drawString(40, y, "Extraordinary:")
            y -= 16
            for line in simpleSplit(text=str(bike.extraordinary),
                                    fontName=c._fontname,
                                    fontSize=c._fontsize,
                                    maxWidth=255):
                c.drawString(50, y, line)
                y -= 14

        # plot image of bike
        if bike.image:
            w = 480  # fixed width
            h = bike.image.height / bike.image.width * w  # keep ratio
            c.drawImage(
                bike.image.url,
                x=321.9, y=450 - h, width=w, height=h
            )

        # End Page
        c.showPage()

    def get(self, request, key, *args, **kwargs):
        # check permission
        if not request.user.has_perm("{}.{}_{}".format("bikes", "change", "Bike")):
            raise PermissionDenied

        if key == 'for_sale':
            queryset = Bike.objects.filter(container__isnull=True, a_plus__exact=True)
        else:
            pks = key.split(',')
            queryset = get_list_or_404(Bike, pk__in=pks)

        # Create a file-like buffer to receive PDF data.
        buf = io.BytesIO()

        a_plus_for_sale = "a_plus_for_sale" in request.GET
        container = request.GET['container'] if 'container' in request.GET else None

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buf, pagesize=landscape(A4))  # W, H = landscape(A4)  # 841.9, 595.27

        if a_plus_for_sale:
            # Add Preface (page by page)
            for page in PdfReader(PROJECT_DIR + "/media/APlusPreface.pdf").pages:
                p.doForm(makerl(p, pagexobj(page)))
                p.showPage()

        # create a pdf page for each bike
        for bike in queryset:
            self.draw_pdf_page(p, bike)

        # Close the PDF object cleanly
        p.save()
        buf.seek(0)

        # define HTT-Response
        response = StreamingHttpResponse(buf, content_type="application/pdf")  # set type to PDF

        # name the document
        name = "{} bikes".format(
            datetime.datetime.now().strftime('%Y-%m-%d')
        )
        if container:
            name = "bikes sold {}".format(
                get_object_or_404(Container, pk=container)
            )
        elif a_plus_for_sale:
            name = "{} A-Plus bikes for sale".format(
                datetime.datetime.now().strftime('%Y-%m-%d')
            )

        # and download it
        response['Content-Disposition'] = "attachment;filename={}.pdf".format(name)
        return response


        )



class BikeListView(ListView):
    """
         Show a list of all containers.

         **Context**
           ``containers``
               A list of instances of :model:`velafrica_sud.Container`



       """

    model = Bike
    template_name = "bikes/bike_list.html"


class BikeCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return BikeCategory.objects.all()
