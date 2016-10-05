# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from velafrica.collection.models import CollectionEvent, EventCategory, Event, Dropoff


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

    class Meta:
        model = Dropoff
