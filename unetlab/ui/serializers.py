"""Serializers, called by API View."""

from rest_framework import serializers
from job.models import Job, Log
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    """Serializer for Log model."""

    class Meta:
        model = User
        fields = "__all__"
        # read_only_fields = [
        #     "id",
        #     "created_at",
        #     "updated_at",
        # ]  # Make some fields read-only
