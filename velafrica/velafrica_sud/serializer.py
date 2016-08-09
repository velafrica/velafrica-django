# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from velafrica.organisation.serializer import OrganisationSerializer
from velafrica.velafrica_sud.models import Container, Forwarder, PartnerSud, Report, Role, Staff

class ContainerSerializer(serializers.ModelSerializer):
	"""
	Todo: write doc.
	"""

	class Meta:
		model = Container


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
    organisation = OrganisationSerializer(many=False, read_only=True)

    class Meta:
        model = PartnerSud       


class RoleSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = Role


class StaffSerializer(serializers.ModelSerializer):
    """
    """
    role = RoleSerializer(many=False, read_only=True)
    class Meta:
        model = Staff


class ReportSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """
    staff = StaffSerializer(source='get_staff', many=True)

    class Meta:
        model = Report       
