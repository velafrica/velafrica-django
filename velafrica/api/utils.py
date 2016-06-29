# -*- coding: utf-8 -*-
from django.apps import apps
from rest_framework import serializers
from rest_framework import generics

def get_serializer_by_model(serialize):
	"""
	"""

	class GenericSerializer(serializers.ModelSerializer):

		class Meta:
			model = serialize

	g = GenericSerializer

	return GenericSerializer
			

def get_serializer(module, classname, __doc__):
	"""
	"""

	model = apps.get_model(module, classname)

	if model:
		return get_serializer_by_model(model)
	else:
		return None


def get_listview_by_model(viewmodel):
	"""
	"""

	class GenericListAPIView(generics.ListCreateAPIView):
		queryset = viewmodel.objects.all()
		serializer_class = get_serializer_by_model(viewmodel)

	return GenericListAPIView


def get_listview(module, classname):
	model = apps.get_model(module, classname)

	if model:
		return get_listview_by_model(model)
	else:
		return None


def get_retrieveview_by_model(viewmodel):
	"""
	"""

	class GenericRetrieveAPIView(generics.RetrieveUpdateAPIView):
		queryset = viewmodel.objects.all()
		serializer_class = get_serializer_by_model(viewmodel)

	return GenericRetrieveAPIView

def get_retrieveview(module, classname):
	model = apps.get_model(module, classname)

	if model:
		return get_listview_by_model(model)
	else:
		return None