# -*- coding: utf-8 -*-
from datetime import timedelta, date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from velafrica.counter.models import Entry
from velafrica.organisation.models import Organisation

# Create your views here.

def counter(request):
  """
  Counter main view
  TODO: fix most productive overall
  """
  org_id = 0
  velos_today = 0
  velos_yesterday = 0
  velos_thisweek = 0
  velos_thismonth = 0
  velos_thisyear = 0
  velos_total = 0

  velos_max = 0
  velos_max_date = date.today()

  entries = Entry.objects.all()

  # get all organisations that already have entries
  org_ids = Entry.objects.order_by().values('organisation').distinct()
  organisations = Organisation.objects.filter(id__in=org_ids)

  if ('id' in request.GET):
    org_id = int(request.GET.get('id'))
    entries = entries.filter(organisation=org_id)

  if (entries.count() > 0):
    now = date.today()
    first_day_of_week = now - timedelta(days=now.weekday())

    for entry in entries:
      # sum up total
      velos_total += entry.amount

      # check if it is the biggest amount
      if entry.amount > velos_max:
        velos_max = entry.amount
        velos_max_date = entry.date

      # check if entry is from current year
      if entry.date.year == now.year:
        velos_thisyear += entry.amount

        # check if entry is from current month
        if entry.date.month == now.month:
          velos_thismonth += entry.amount

      # check if entry is from current week
      if entry.date >= first_day_of_week:
        velos_thisweek += entry.amount

      # check if latest entry was from today
      if entry.date == now:
        velos_today += entry.amount

      # get entry from yesterday
      if entry.date == (now - timedelta(days=1)):
        velos_yesterday += entry.amount

  return render_to_response('counter/index.html', {
    'org_id': org_id,
    'organisations' : organisations,
    'velos_total': velos_total,
    'velos_thisyear': velos_thisyear,
    'velos_thismonth': velos_thismonth,
    'velos_thisweek': velos_thisweek,
    'velos_yesterday': velos_yesterday,
    'velos_today': velos_today,
    'velos_max': velos_max,
    'velos_max_date': velos_max_date,
    }, context_instance=RequestContext(request)
  )

@login_required
def counter_form(request):
  """
  Show to create new entries.
  """
  pass