from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from velafrica.stock.models import Warehouse

class WarehouseSerializer(serializers.ModelSerializer):
	"""
	Todo: write doc.
	"""

	class Meta:
		model = Warehouse