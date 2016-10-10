# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from velafrica.collection.models import CollectionEvent, EventCategory, Event, Dropoff
from velafrica.organisation.serializer import AdressSerializer

class EventCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EventCategory


class EventSerializer(serializers.ModelSerializer):

    category = EventCategorySerializer(many=False)

    class Meta:
        model = Event


class CollectionEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionEvent


class DropoffSerializer(serializers.ModelSerializer):

    address = AdressSerializer(many=False, read_only=True)

    class Meta:
        model = Dropoff
