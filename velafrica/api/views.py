# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from rest_framework import permissions, generics
from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import CoreJSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response


class DjangoModelPermissionsMixin(generics.GenericAPIView):
    """
    Permission Mixin
    """
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions,)


schema_url_patterns = [
    url(r'^api/', include('velafrica.api.urls')),
]

generator = schemas.SchemaGenerator(title='Velafrica API', urlconf='velafrica.api.urls')


@api_view()
@renderer_classes([BrowsableAPIRenderer, CoreJSONRenderer])
def schema_view(request):
    schema = generator.get_schema(request)
    return response.Response(schema)


@api_view(('GET',))
def api_root(request, format=None):
    """
    The REST API of the Velafrica tracking system (<a href="http://tracking.velafrica.ch">tracking.velafrica.ch</a>)

    It has been built with <b>Django</b> and <b>Django Rest Framework</b> by <a href="http://platzh1rsch.ch">platzh1rsch</a>, during civil service and is still updated from time to time.

    All list endpoints accept GET & POST, all detail endpoints accept GET & PUT - if you have the according permissions.

    Go to /api/swagger to see the Swagger documentation of the api.

    -------------------

    There is a github repository with all the code of this project.

    If you are in need of any adjustments or bug fixes, or you need access to the repository, do not hesitate to drop me an email: <i>chregi.glatthard(at)gmail.com</i>.

    If you have more general questions you can also contact Nikolai Räber <i>(nikolai.raeber(at)velafrica.ch)</i>.

    """

    #response = utils.get_api_root_listing_from_urls(request, format)
    response = "Go to /api/swagger to see all the available endpoints"

    return Response(response)
