from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from velafrica.organisation.models import Person, Organisation

class OrganisationSerializer(serializers.ModelSerializer):
	"""
	Todo: write doc.
	"""

	class Meta:
		model = Organisation


class PersonSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = Person
