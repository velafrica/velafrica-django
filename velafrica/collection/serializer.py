# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from velafrica.collection.models import CollectionEvent


class CollectionEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionEvent
