# -*- coding: utf-8 -*-
from rest_framework import permissions, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from velafrica.api import utils


class DjangoModelPermissionsMixin(generics.GenericAPIView):
    """
    Permission Mixin
    """
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions,)


@api_view(('GET',))
def api_root(request, format=None):
    """
    This is the API of Velafrica (www.velafrica.ch)

    If you build something cool with it and want to show it to us, please do not hesitate!

    Send a link with description to nikolai.raeber (at) velafrica.ch

    Have fun!
    """

    response = utils.get_api_root_listing_from_urls(request, format)

    return Response(response)