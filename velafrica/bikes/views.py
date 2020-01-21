# -*- coding: utf-8 -*-

from dal import autocomplete
from django.views.generic import ListView

from velafrica.bikes.models import Bike, BikeCategory
from velafrica.core.pdf_utils import render_to_pdf


def bikes_pdf(request, queryset, title=None, subtitle=None, filename=""):
    return render_to_pdf(
        request,
        template="bikes/bikes_pdf.html",
        context={
            "title": title,
            "subtitle": subtitle,
            "pagesize": "A4 landscape",
            "logo": 'img/velafrica_RGB.jpg',
            "stylesheets": ("css/bike_plot.css",),
            "bikes": queryset,
        },
        filename="{}.pdf".format(filename) if filename else None,
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
