from datetime import timedelta, date
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

"""
Counter
"""

def counter(request):
  velos_today = 0
  velos_yesterday = 0
  velos_thisweek = 0
  velos_thismonth = 0
  velos_thisyear = 0
  velos_total = 0

  entries = Entry.objects.all()
  latest = entries.first()
  now = date.today()
  first_day_of_week = now - timedelta(days=now.weekday())

  # check if latest entry was from today
  if now == latest.date:
      velos_today = latest.amount

  for entry in entries:
    # sum up total
    velos_total += entry.amount

    # check if entry is from current year
    if entry.date.year == now.year:
      velos_thisyear += entry.amount

      # check if entry is from current month
      if entry.date.month == now.month:
        velos_thismonth += entry.amount

    # check if entry is from current week
    if entry.date >= first_day_of_week:
      velos_thisweek += entry.amount

    # todo: get entry from yesterday
    if entry.date == (now - timedelta(days=1)):
      velos_yesterday += entry.amount

  return render_to_response('counter/index.html', { 
    'velos_total': velos_total,
    'velos_thisyear': velos_thisyear,
    'velos_thismonth': velos_thismonth,
    'velos_thisweek': velos_thisweek,
    'velos_yesterday': velos_yesterday,
    'velos_today': velos_today
    })
