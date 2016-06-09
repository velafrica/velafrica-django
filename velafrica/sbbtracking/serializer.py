from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from velafrica.sbbtracking.models import Tracking, TrackingEvent, TrackingEventType


class TrackingSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = Tracking
        fields = [ "id", "tracking_no", "number_of_velos", "note", "complete", "vpn", "container", "velo_type", "last_event" ]


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