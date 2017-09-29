# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext
from dal import autocomplete
from django.db.models import Q


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

class DriverAutocomplete(autocomplete.Select2QuerySetView):
    """
    Used for django-admin-autocomplete
    """
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if self.request.user.is_superuser:
            qs = Driver.objects.all()
            # other users with a correlating person should only see their organisation
        elif hasattr(self.request.user, 'person') and self.request.user.is_authenticated():
            qs = Driver.objects.filter(organisation=self.request.user.person.organisation.id)
            # users with no superuser role and no related person should not see any organisations
        else:
            return Driver.objects.none()

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(organisation__name__icontains=self.q))

        return qs