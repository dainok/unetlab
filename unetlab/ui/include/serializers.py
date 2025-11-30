"""Generic serializer for REST API views."""

from rest_framework import serializers


class ObjectSerializer(serializers.ModelSerializer):
    """Base serializer for Django models."""

    class Meta:
        """Meta options."""

        model = None
        fields = "__all__"
