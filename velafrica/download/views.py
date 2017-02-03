# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext

from velafrica.download.models import File


@login_required
def downloads(request):
  """
  Show all available downloads.
  Login is required to see this view.
  
  **Context**
  
  ``files``
    A list of all instances of :model:`download.File` .
  
  **Template**

  :template:`download/index.html`
  """
  files = File.objects.all()
  return render(
    request,
    'download/index.html', 
    {'files': files}
    )