# -*- coding: utf-8 -*-
from rest_framework import serializers

from velafrica.bikes.models import Bike


class BikeSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = Bike
        fields = '__all__'
