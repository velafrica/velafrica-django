# -*- coding: utf-8 -*-
from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import CoreJSONRenderer
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, CoreJSONRenderer])
def schema_view(request):
    '''
    Swagger Documentation of the Velafrica API.
    :param request:
    :return:
    '''
    generator = schemas.SchemaGenerator(title='Velafrica API', url='/api', urlconf='velafrica.api.urls')
    return response.Response(generator.get_schema(request=request))
