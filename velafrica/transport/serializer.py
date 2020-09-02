# -*- coding: utf-8 -*-
from rest_framework import serializers

from velafrica.transport.models import Ride


class RideSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = Ride
        fields = '__all__'
