# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext

from velafrica.velafrica_sud.models import Container


@login_required
def container(request):
  """
  Show a list of all containers.

  **Context**
    ``containers``
        A list of instances of :model:`velafrica_sud.Container`

      ``bicycles_total``
        The sum of all bicycles transported in all containers.

  """
  containers = Container.objects.all()
  bicycles_total = 0
  time_to_customer_total = 0
  time_to_customer_entries = 0
  time_to_customer_average = None

  for c in containers:
      bicycles_total += c.velos_loaded
      if c.time_to_customer:
          time_to_customer_total += c.time_to_customer
          time_to_customer_entries += 1

  if time_to_customer_entries > 0:
    time_to_customer_average = time_to_customer_total / time_to_customer_entries

  context = {
      'containers': containers,
      'bicycles_total': bicycles_total,
      'time_to_customer_average': time_to_customer_average
  }

  return render(request, 'velafrica_sud/container.html', context)
