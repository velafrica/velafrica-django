# -*- coding: utf-8 -*-
import mailchimp
from django.db.models import Q
from django.utils import timezone
from itertools import chain
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from velafrica.collection.models import Dropoff, CollectionEvent
from velafrica.collection.serializer import DropoffSerializer
from velafrica.core.settings import MAILCHIMP_LIST_ID


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_dropoffs(request):
    """
    Get a list of all dropoffs from the database
    TODO: fix AttributeError: 'str' object has no attribute 'values'

    :param request:
    :return:
    """
    q = Q(temp=True) & Q(temp_end__lte=timezone.now().date().strftime('%Y-%m-%d'))
    all = Dropoff.objects.filter(active=True).exclude(q)

    coll_drop = list()
    for collectionevent in CollectionEvent.objects.filter(date_end__gte=timezone.now().date().strftime('%Y-%m-%d')) \
            .exclude(event__address=None):
        new_drop = Dropoff(
            name=collectionevent.event.name,
            sbb=False,
            pickup=False,
            temp=True,
            temp_start=collectionevent.date_start,
            temp_end=collectionevent.date_end,
            opening_time=collectionevent.time,
            address=collectionevent.event.address
        )
        # make a negative id to let javascript know that this is a collectionevent
        new_drop.id = -1 * collectionevent.id
        coll_drop.append(new_drop)
    ret = list(chain(all, coll_drop))

    serializer = DropoffSerializer(ret, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def subscribe_newsletter(request):
    """

    :param request:
    :return:
    """
    email = request.POST.get('email', False)
    if email:
        if MAILCHIMP_LIST_ID:
            list = mailchimp.utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
            # TODO: proper exception handling
            return Response(list.subscribe(email, {'EMAIL': email}, double_optin=False))
        else:
            return Response(False)
    else:
        return Response(False)
