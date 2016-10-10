# -*- coding: utf-8 -*-
from rest_framework import serializers

from velafrica.organisation.models import Person, Organisation, Address, Country


class PersonSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = Person


class CountrySerializer(serializers.ModelSerializer):
	"""
	"""

	class Meta:
		model = Country

class AdressSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """
    googlemaps_url = serializers.ReadOnlyField(source='get_googlemaps_url')
    country = CountrySerializer(many=False, read_only=False)

    class Meta:
        model = Address


class OrganisationSerializer(serializers.ModelSerializer):
	"""
	Todo: write doc.
	"""
	address = AdressSerializer(many=False, read_only=False)
	#partnersud = PartnerSudSerializer(many=False, read_only=False)

	class Meta:
		model = Organisation