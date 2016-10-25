# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

def render_template(request):
    template_name = 'index'
    if request.path != '':
      template_name = request.path
    return render_to_response('public_site' + template_name + '.html', {

    }, context_instance=RequestContext(request))
