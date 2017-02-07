# -*- coding: utf-8 -*-
from rest_framework import serializers

from velafrica.organisation.serializer import OrganisationSerializer
from velafrica.velafrica_sud.models import Container, Forwarder, PartnerSud, Report, Role, ReportStaff, PartnerStaff


class ContainerSerializer(serializers.ModelSerializer):
	"""
	Todo: write doc.
	"""

	class Meta:
		model = Container
        fields = '__all__'


class ForwarderSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = Forwarder
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = Role
        fields = '__all__'


class PartnerStaffSerializer(serializers.ModelSerializer):
    """
    """
    role = RoleSerializer(many=False, read_only=True)
    #staff = PartnerStaffSerializer(source='get_staff', many=True)
    class Meta:
        model = PartnerStaff
        fields = '__all__'


class PartnerSudSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """
    organisation = OrganisationSerializer(many=False, read_only=True)

    class Meta:
        model = PartnerSud
        fields = '__all__'


class ReportStaffSerializer(serializers.ModelSerializer):
    """
    """
    role = RoleSerializer(many=False, read_only=True)

    class Meta:
        model = ReportStaff
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """
    staff = ReportStaffSerializer(source='get_staff', many=True)

    class Meta:
        model = Report
        fields = '__all__'