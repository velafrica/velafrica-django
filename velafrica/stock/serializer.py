from rest_framework import serializers

from velafrica.stock.models import Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
	"""
	Todo: write doc.
	"""

	class Meta:
		model = Warehouse