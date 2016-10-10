# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
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
  for c in containers:
    bicycles_total += c.velos_loaded

  return render_to_response('velafrica_sud/container.html', {
    'containers': containers,
    'bicycles_total': bicycles_total,
    }, context_instance=RequestContext(request)
  )