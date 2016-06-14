# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.
@login_required
def stock(request):
  """
  Stock
  """
  stock = Stock.objects.all()
  return render_to_response('stock/index.html', { 
    'stock': stock
    }, context_instance=RequestContext(request)
  )