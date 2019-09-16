# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView

from velafrica.bikes.models import Bike


class BikeListView(ListView):
    """
         Show a list of all containers.

         **Context**
           ``containers``
               A list of instances of :model:`velafrica_sud.Container`



       """

    model = Bike
    template_name = "bikes/bike_list.html"
