# -*- coding: utf-8 -*-
from django.apps import apps
from rest_framework import generics
from rest_framework import serializers
from django.urls import reverse

def get_serializer_by_model(serialize):
    """

    :param serialize:
    :return:
    """

    class GenericSerializer(serializers.ModelSerializer):

        class Meta:
            model = serialize
            fields = '__all__'

    g = GenericSerializer

    return GenericSerializer
            

def get_serializer(module, classname, __doc__):
    """

    :param module:
    :param classname:
    :param __doc__:
    :return:
    """

    model = apps.get_model(module, classname)

    if model:
        return get_serializer_by_model(model)
    else:
        return None


def get_listview_by_model(viewmodel):
    """

    :param viewmodel:
    :return:
    """

    class GenericListAPIView(generics.ListCreateAPIView):
        queryset = viewmodel.objects.all()
        serializer_class = get_serializer_by_model(viewmodel)

    return GenericListAPIView


def get_listview(module, classname):
    """

    :param module:
    :param classname:
    :return:
    """
    model = apps.get_model(module, classname)

    if model:
        return get_listview_by_model(model)
    else:
        return None


def get_retrieveview_by_model(viewmodel):
    """

    :param viewmodel:
    :return:
    """

    class GenericRetrieveAPIView(generics.RetrieveUpdateAPIView):
        queryset = viewmodel.objects.all()
        serializer_class = get_serializer_by_model(viewmodel)

    return GenericRetrieveAPIView


def get_retrieveview(module, classname):
    """

    :param module:
    :param classname:
    :return:
    """
    model = apps.get_model(module, classname)

    if model:
        return get_listview_by_model(model)
    else:
        return None


def load_url_pattern_names(namespace, patterns):
    """
    Retrieve a list of urlpattern names
    """
    url_names = []

    for pat in patterns:
        if pat.__class__.__name__ == 'RegexURLResolver':  # load patterns from this RegexURLResolver
            url_names.append(load_url_pattern_names(pat.namespace, pat.url_patterns))
        elif pat.__class__.__name__ == 'RegexURLPattern':  # load name from this RegexURLPattern
            # fully qualified pattern name :) (namespace::name)

            if pat.name is not None and pat.name not in url_names:
                url_names.append((pat.name, pat.callback.__doc__))
    return namespace, url_names


def get_api_root_listing_from_urls(request, format):
    """
    Get a nested dictionary of all url routes, grouped by namespace.

    :param request:
    :param format:
    :return:
    """
    from velafrica.api import urls

    # access the "urlpatterns" from the ROOT_URLCONF
    url_tree = load_url_pattern_names(None, urls.urlpatterns)

    response = {}
    for namespace_set in url_tree[1]:
        namespace = namespace_set[0]

        urls = namespace_set[1]
        namespace_urls = {}
        for ur in urls:
            if namespace:
                fqpn = 'api:{}:{}'.format(namespace, ur[0])
                rev = ""

                try:    # this will work for list views
                    rev = reverse(str(fqpn))
                except: # if it is a detail view, we need to provide a pk
                    rev = reverse(str(fqpn), kwargs={'pk': 1})

                description = "{}".format(ur[1])
                namespace_urls[rev] = description.strip()
        response[namespace] = namespace_urls

    return response
