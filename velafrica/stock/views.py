# -*- coding: utf-8 -*-
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from velafrica.stock.models import Product, Warehouse, Stock


@login_required
def stock(request):
  """
  Stock
  """
  stock = Stock.objects.all()

  if request.user.is_superuser or request.user.has_perm('stock.is_admin'):
  	stock = Stock.objects.all()
  # other users with a correlating person should only see their organisations entries
  elif hasattr(request.user, 'person'):
    stock = stock.filter(warehouse__organisation=request.user.person.organisation)
  # users with no superuser role and no related person should not see any entries
  else:	
  	stock = stock.none()
            
  return render_to_response('stock/index.html', { 
    'stock': stock
    }, context_instance=RequestContext(request)
  )


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Product.objects.none()

        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(Q(name__contains=self.q) | Q(articlenr__contains=self.q))

        return qs

class WarehouseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Product.objects.none()

        qs = Warehouse.objects.all()

        if self.q:
            qs = qs.filter(Q(name__contains=self.q) | Q(organisation__name__contains=self.q))

        return qs