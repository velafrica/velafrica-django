# -*- coding: utf-8 -*-
from rest_framework import serializers

from velafrica.counter.models import Entry


class EntrySerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = Entry
        fields = '__all__'
