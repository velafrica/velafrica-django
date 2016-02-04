import datetime
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.core import serializers

from velafrica.stock.models import Category, Product
from velafrica.counter.models import Entry

def home(request):
  return render_to_response('base.html')

def counter(request):
  velos_today = 0
  velos_total = 0

  entries = Entry.objects.all()
  today = entries.first()
  now = datetime.datetime.now()

  if now.date() == today.date:
      velos_today = today.amount

  for entry in entries:
    velos_total += entry.amount
  velos_total_str = str(velos_total)
  return render_to_response('counter/index.html', { 'velos_total': velos_total_str, 'velos_today': velos_today })
