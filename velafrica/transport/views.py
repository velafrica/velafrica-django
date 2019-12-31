# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext
from dal import autocomplete
from django.db.models import Q


from velafrica.transport.models import Ride, Car, Driver


def get_velo_count(rides):
    velos = 0
    for r in rides:
        velos += r.velos
    return velos


def get_charts(cars, rides):
    charts = {}
    # by car
    charts_car = {}
    for c in cars:
        rs = rides.filter(car=c.id)
        charts_car[c.name] = rs.count()
    charts['Cars'] = charts_car

    # by driver
    charts_driver = {}
    for d in Driver.objects.all():
        rs = rides.filter(driver=d.id)
        charts_driver[d.name] = rs.count()
    charts['Driver'] = charts_driver

    # by spare parts / no spare parts
    charts['Freight'] = {
        'Spare Parts': rides.filter(spare_parts=True).count(),
        'Velos': rides.filter(spare_parts=False).count()
    }
    return charts

@login_required
def transport(request):
    """
    Show transport statistics.
      
      **Context**

      ``rides``
          List of all instances of :model:`transport.Ride`

      ``velos``
          Sum of velos transported in instances of :model:`transport.Ride`
      
      ``cars``
          List of all instances of :model:`Car`
      
      ``charts``
        Various data for charts, that will be displayed in :template:`transport/index.html`, using ``Chart.js``

    **Template**
  
    :template:`transport/index.html`
    """
    rides = Ride.objects.all()[:100]
    rides_count = Ride.objects.all().count

    # TODO: refactor get_velo_count
    # velos = get_velo_count(rides)
    velos = 0

    cars = Car.objects.all()
  
    # chart data
    # TODO: refactor get_charts
    # charts = get_charts(cars, rides)
    charts = {}

    return render(request, 'transport/index.html', {
        'rides': rides,
        'rides_count': rides_count,
        'velos': velos,
        'cars': cars,
        'charts': charts,
        }
    )


class DriverAutocomplete(autocomplete.Select2QuerySetView):
    """
    Used for django-admin-autocomplete
    """
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if self.request.user.is_superuser:
            qs = Driver.objects.all()
            # other users with a correlating person should only see their organisation
        elif hasattr(self.request.user, 'person') and self.request.user.is_authenticated:
            qs = Driver.objects.filter(organisation=self.request.user.person.organisation.id)
            # users with no superuser role and no related person should not see any organisations
        else:
            return Driver.objects.none()

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(organisation__name__icontains=self.q))

        return qs


class CarAutocomplete(autocomplete.Select2QuerySetView):
    """
    Used for django-admin-autocomplete
    """
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if self.request.user.is_superuser:
            qs = Car.objects.all()
            # other users with a correlating person should only see their organisation
        elif hasattr(self.request.user, 'person') and self.request.user.is_authenticated:
            qs = Car.objects.filter(organisation=self.request.user.person.organisation.id)
            # users with no superuser role and no related person should not see any organisations
        else:
            return Car.objects.none()
        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(organisation__name__icontains=self.q))

        return qs


def print_transport_request_view(request, rides, *args, **kwargs):
    return render(
        request,
        template_name="transport/print-request.html",
        context={
            "title": "Transport Request",
            "body_attributes": {
               "onload": "window.print()"
            },
            "stylesheets": ["/static/css/transport_request.css"],
            "logo": "/static/img/velafrica_logo_small.png",
            "rides": Ride.objects.filter(pk__in=rides.split(","))
        }
    )

