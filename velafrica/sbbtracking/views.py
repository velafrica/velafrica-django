# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext

from velafrica.sbbtracking.models import Tracking, TrackingEvent


def tracking(request, tracking_no=0):
  """
  Show tracking landing page. Displays a text input field where the user can enter his tracking number.

  If tracking number is provided as GET parameter, the view will display the according tracking information if found, or an error message otherwise.

  :model:`sbbtracking.Tracking`

  :model:`sbbtracking.TrackingEvent`

  :template:`sbbtracking/index.html`
  """
  tracking = []
  tracking_events = []
  tno = tracking_no
  direct_access = False   # Indicates if visitor accessed tracking over direct url (/tracking/XYZ)

  if tno == 0:
    if 'tracking_no' in request.POST:
      tno = request.POST['tracking_no']
    else:
      pass

  if tno and tno != 0:
    tno = str(tno)
    tno = tno.upper()

    tracking = Tracking.objects.filter(tracking_no=tno).first()
    direct_access = True
    if tracking: 
      tracking_events = TrackingEvent.objects.filter(tracking=tracking.id)
    else:
      messages.add_message(request, messages.ERROR, "Kein Tracking mit der Nummer {} gefunden.".format(tno))

  return render_to_response('sbbtracking/index.html', {
    'tno': tno,
    'tracking': tracking,
    'tracking_events': tracking_events,
    'direct_access': direct_access,
    }, context_instance=RequestContext(request)
  )