"""Serializers, called by API View."""

from rest_framework import serializers
from lab.models import Labs


class LabSerializer(serializers.ModelSerializer):
    """Serializer for Template model."""

    class Meta:
        model = Lab
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
        ]  # Make some fields read-only
