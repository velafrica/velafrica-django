# -*- coding: utf-8 -*-

from dal import autocomplete
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Count, Sum
from django.shortcuts import render

from velafrica.core.pdf_utils import render_to_pdf
from velafrica.transport.models import Ride, Car, Driver, VeloState, RequestCategory


def get_charts():
    return {
        'Cars': {
            c.name: c.ride__count
            for c in Car.objects.annotate(Count('ride'))
        },
        # There're probably too many drivers
        # 'Driver': {
        #     d.name: d.ride__count
        #     for d in Driver.objects.annotate(Count('ride'))
        # },
        'Freight': {
            'Spare Parts': Ride.objects.filter(spare_parts=True).count(),
            'No Spare Parts': Ride.objects.filter(spare_parts=False).count()
        }
    }


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
    return render(
        request,
        template_name='transport/index.html',
        context={
            'rides': Ride.objects.all()[:100],
            'rides_count': Ride.objects.count(),
            'velos': Ride.objects.aggregate(velo_count=Sum('velos'))['velo_count'],
            'cars': Car.objects.all(),
            'charts': {}  # get_charts() disabled for now
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


class RequestCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return RequestCategory.objects.all()


class VeloStateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return VeloState.objects.all()


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


@permission_required("transport.view_ride")
def transport_request_pdf_view(request, rides, title):
    return render_to_pdf(
        request=request,
        template="transport/print-request.html",
        context={
            "title": title,
            "stylesheets": (
                'css/transport_request.css',
            ),
            "logos": (
                "img/velafrica_SW.png",  # os.path.join(MEDIA_ROOT, "velafrica_SW.png"),
                "img/Drahtesel_A4_schwarz.png",  # os.path.join(MEDIA_ROOT, "Drahtesel_A4_schwarz.png"),
            ),
            "rides": [
                r.prepare_for_view()
                for r in rides
            ]
        },
        filename="{}.pdf".format(title)
    )
