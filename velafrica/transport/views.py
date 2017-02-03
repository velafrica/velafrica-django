# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext

from velafrica.transport.models import Ride, Car, Driver


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
    rides = Ride.objects.all()
    velos = 0
    for r in rides:
        velos += r.velos
    cars = Car.objects.all()
  
    # chart data
  
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
  
    return render(request, 'transport/index.html', {
        'rides': rides,
        'velos': velos,
        'cars': cars,
        'charts': charts,
        }
    )
  