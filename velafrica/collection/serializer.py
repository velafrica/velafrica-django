# -*- coding: utf-8 -*-
from rest_framework import serializers

from velafrica.collection.models import CollectionEvent, EventCategory, Event, Dropoff
from velafrica.organisation.serializer import AdressSerializer


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer(many=False)

    class Meta:
        model = Event
        fields = '__all__'


class EventPublicSerializer(serializers.ModelSerializer):
    address = AdressSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'host', 'address', 'address_notes')


class CollectionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionEvent
        fields = '__all__'


class CollectionEventPublicSerializer(serializers.ModelSerializer):
    event = EventPublicSerializer(many=False)

    class Meta:
        model = CollectionEvent
        fields = ('id', 'date_start', 'date_end', 'time', 'website', 'event')


class DropoffSerializer(serializers.ModelSerializer):
    address = AdressSerializer(many=False, read_only=True)

    class Meta:
        model = Dropoff
        fields = '__all__'
