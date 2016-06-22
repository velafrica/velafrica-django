from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from velafrica.velafrica_sud.models import Container, Country, Forwarder, PartnerSud

class ContainerSerializer(serializers.ModelSerializer):
	"""
	Todo: write doc.
	"""

	class Meta:
		model = Container


class CountrySerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = Country


class ForwarderSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = Forwarder


class PartnerSudSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """
    
    class Meta:
        model = PartnerSud       
