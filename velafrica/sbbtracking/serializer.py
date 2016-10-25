# -*- coding: utf-8 -*-
from rest_framework import serializers

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
        read_only = ["next_tracking_eventtype_options", "last_event", "complete"]


class TrackingDetailSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """
    velo_type = VeloTypeSerializer(many=False, read_only=False)
    last_event = TrackingEventSerializer(many=False, read_only=True)
    next_tracking_eventtype_options = TrackingEventTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Tracking
        read_only = ["next_tracking_eventtype_options", "last_event", "complete"]
