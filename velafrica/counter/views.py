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
  """

  org_id = 0
  if ('id' in request.GET):
    org_id = int(request.GET.get('id'))
  
  statistics = Entry.get_statistics(org_id)

  print "STATS: {}".format(statistics)

  return render_to_response('counter/index.html', {
    'org_id': statistics["org_id"],
    'organisations' : statistics["organisations"],
    'velos_total': statistics["velos_total"],
    'velos_thisyear': statistics["velos_thisyear"],
    'velos_thismonth': statistics["velos_thismonth"],
    'velos_thisweek': statistics["velos_thisweek"],
    'velos_yesterday': statistics["velos_yesterday"],
    'velos_today': statistics["velos_today"],
    'velos_max': statistics["velos_max"],
    'velos_max_date': statistics["velos_max_date"],
    }, context_instance=RequestContext(request)
  )

@login_required
def counter_form(request):
  """
  Show to create new entries.
  """
  pass