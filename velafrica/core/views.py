# -*- coding: utf-8 -*-
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
  """
  Landing page

  :template:`base.html`
  """
  return render_to_response('base.html', context_instance=RequestContext(request))


@login_required
def profile(request):
  """
  Show a welcome page for logged in users with a link to the admin area (if they are staff).

  :template:`auth/profile.html`
  """
  return render_to_response(
    'auth/profile.html',
    context_instance=RequestContext(request)
    )


def accounts_logout(request):
  """
  Logout viev according to https://docs.djangoproject.com/en/1.9/topics/auth/default/

  :view:`django.contrib.auth.views.login`
  """
  logout(request)
  return redirect('auth:django.contrib.auth.views.login')
