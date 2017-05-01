# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from velafrica.collection.models import CollectionEvent

@login_required
def collection(request):
  """
  Show a list of all collection events.

  **Context**
    ``containers``
        A list of instances of :model:`velafrica_sud.Container`

      ``bicycles_total``
        The sum of all bicycles transported in all containers.

  """
  collection_events = CollectionEvent.objects.all()

  return render(request, 'collection/index.html', {'collection_events': collection_events})
