from rest_framework import serializers
from django_admin_conf_vars.models import ConfigurationVariable
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class ConfigurationVariableSerializer(serializers.ModelSerializer):
    """
    Todo: write doc.
    """

    class Meta:
        model = ConfigurationVariable