# -*- coding: utf-8 -*-
from itertools import chain

from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.template import RequestContext

from velafrica.stock.models import Product, Warehouse, Stock, StockChange, StockListPosition
from velafrica.transport.models import Ride
from velafrica.velafrica_sud.models import Container


@login_required
def stock(request):
    """
    Show stock overview.

    **Context**

    ``stock``
        List of instances of :model:`stock.Stock`

    ``warehouses``
        List of instances of :model:`stock.Warehouse`

    **
    """
    stock = Stock.objects.all()
    warehouse_ids = stock.order_by().values('warehouse').distinct()
    warehouses = Warehouse.objects.filter(id__in=warehouse_ids)

    if request.user.is_superuser or request.user.has_perm('stock.is_admin'):
          stock = Stock.objects.all()
    # other users with a correlating person should only see their organisations entries
    elif hasattr(request.user, 'person'):
        stock = stock.filter(warehouse__organisation=request.user.person.organisation)
    # users with no superuser role and no related person should not see any entries
    else:
          stock = stock.none()
            
    return render(request, 'stock/index.html', {
        'stock': stock, 
        'warehouses': warehouses,
        }
    )


@login_required
def warehouses(request):
    """
    Show a list of all warehouses.
    
    **Context**
    
    ``warehouses``
        List of instances of :model:`stock.Warehouse`
  
    **Template**

    :template:`stock/warehouses.html`
    """
    return render(request, 'stock/warehouses.html', {
        'warehouses': Warehouse.objects.all(),
        }
    )

@login_required
def warehouse(request, pk):
    """
    Show details of a specific Warehouse and several statistics.
  
    **Context**

    ``warehouse``
        List of instances of :model:`stock.Warehouse`
  
    ``rides``
        List of instances of :model:`stock.Ride`

    ``rides_in`` 
        Number of instances of :model:`transport.Ride` going in to this warehouse.

    ``rides_out``
        Number of instances of :model:`transport.Ride` going out of this warehouse.

    ``velos_in`` 
        Number of velos having been brought in to this warehouse in :model:`transport.Ride`

    ``velos_out``
        Number of velos having been brought away from this warehouse in :model:`transport.Ride`


    ``velos_stock`` 
        Difference of ``velos_in`` and ``velos_out``

    ``container_out``
        Number of instances of :model:`stock.Container` having been shipped from this warehouse.
  
    ``container_velos_out``
        Sum of all velos having been shipped from this warehouse in containers.

    **Template**

    :template:`stock/warehouse_detail.html`
    """
    warehouse = Warehouse.objects.get(id=pk)
    rides_in = 0
    rides_out = 0
    velos_in = 0
    velos_out = 0
    velo_stock = 0
    container_out = 0
    container_velos_out = 0
    rides = Ride.objects.none()

    if not warehouse: 
        messages.add_message(request, messages.ERROR, "Kein Lager mit der ID {} gefunden.".format(pk))
    else:
        rides_in_list = Ride.objects.filter(to_warehouse=pk)
        rides_out_list = Ride.objects.filter(from_warehouse=pk)
        rides_in = rides_in_list.count()
        rides_out = rides_out_list.count()
        for r in rides_in_list:
            velos_in += r.velos
        for r in rides_out_list:
            velos_out += r.velos

    containers = Container.objects.filter(warehouse_from=pk)
    container_out = containers.count()
    for c in containers:
        container_velos_out += c.velos_loaded

    velo_stock = velos_in - velos_out - container_velos_out

    rides = sorted(
        chain(rides_in_list, rides_out_list),
        key=lambda instance: instance.date)

    # get stock statistics 
    # TODO: needs performance improvement, also create separate function
    stockchanges = StockChange.objects.filter(warehouse=warehouse)
    stockchanges_in = stockchanges.filter(stock_change_type='in')
    stockchanges_out = stockchanges.filter(stock_change_type='out')

    stocklists_in = []
    for sci in stockchanges_in:
        stocklists_in.append(sci.stocklist)

    stocklists_out = []
    for sco in stockchanges_out:
        stocklists_out.append(sco.stocklist)
    
    listpos_in = StockListPosition.objects.filter(stocklist__in=stocklists_in)
    listpos_out = StockListPosition.objects.filter(stocklist__in=stocklists_out)

    # prepare dict in form of "product" : (current stock, total in, total out)
    stock_movements = {}

    stocks = Stock.objects.filter(warehouse=warehouse)

    for s in stocks:
        s_in = 0
        s_out = 0
        for l in listpos_in.filter(product=s.product):
            s_in += l.amount
        for l in listpos_out.filter(product=s.product):
            s_out += l.amount

        # save in tuple (in, out, diff)
        stock_movements[s] = (s_in, s_out, (s_in - s_out))

    return render(request, 'stock/warehouse_detail.html', {
        'warehouse': warehouse,
        'rides': rides,
        'rides_in': rides_in,
        'rides_out': rides_out,
        'stock_movements': stock_movements,
        'velos_in': velos_in,
        'velos_out': velos_out,
        'velo_stock': velo_stock,
        'container_out': container_out,
        'container_velos_out': container_velos_out,
        }
    )



class ProductAutocomplete(autocomplete.Select2QuerySetView):
    """
    Used for django-admin-autocomplete
    """
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Product.objects.none()

        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(articlenr__icontains=self.q))

        return qs

class WarehouseAutocomplete(autocomplete.Select2QuerySetView):
    """
    Used for django-admin-autocomplete
    """
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Product.objects.none()

        qs = Warehouse.objects.all()

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(organisation__name__icontains=self.q))

        return qs