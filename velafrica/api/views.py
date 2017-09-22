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
    The REST API of the Velafrica tracking system (<a href="http://tracking.velafrica.ch">tracking.velafrica.ch</a>)

    It has been built with <b>Django</b> and <b>Django Rest Framework</b> by <a href="http://platzh1rsch.ch">platzh1rsch</a>, during civil service and is still updated from time to time.

    All list endpoints accept GET & POST, all detail endpoints accept GET & PUT - if you have the according permissions.

    -------------------

    There is a github repository with all the code of this project.

    If you are in need of any adjustments or bug fixes, or you need access to the repository, do not hesitate to drop me an email: <i>chregi.glatthard(at)gmail.com</i>.

    If you have more general questions you can also contact Nikolai Räber <i>(nikolai.raeber(at)velafrica.ch)</i>.

    """

    response = utils.get_api_root_listing_from_urls(request, format)

    return Response(response)