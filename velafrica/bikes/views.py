# -*- coding: utf-8 -*-

from dal import autocomplete
from django.views.generic import ListView

from velafrica.bikes.models import Bike, BikeCategory
from velafrica.bikes.render_pdf import render_bikes_to_pdf_with_reportlab
from velafrica.core.pdf_utils import make_response


def bikes_pdf(request, queryset, title=None, subtitle=None, filename=""):
    return make_response(
        render_bikes_to_pdf_with_reportlab(
            queryset,
            fields={
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
            },
            title=title,
            subtitle=subtitle
        ),
        filename="{}.pdf".format(filename) if filename else None
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
