from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from velafrica.sbbtracking.models import Tracking, TrackingEvent, TrackingEventType, VeloType

class VeloTypeSerializer(serializers.ModelSerializer):
	"""
	Todo: write doc.
	"""

	class Meta:
		model = VeloType


class TrackingEventSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = TrackingEvent


class TrackingEventTypeSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = TrackingEventType


class TrackingSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """
    next_tracking_eventtype_options = TrackingEventTypeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tracking
        fields = [ "id", "tracking_no", "number_of_velos", "note", "complete", "vpn", "container", "velo_type", "last_event", "next_tracking_eventtype_options" ]
        read_only = ["next_tracking_eventtype_options", "last_event"]


class TrackingDetailSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """
    velo_type = VeloTypeSerializer(many=False, read_only=True)
    last_event = TrackingEventSerializer(many=False, read_only=True)

    class Meta:
        model = Tracking
