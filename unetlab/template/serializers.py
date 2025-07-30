"""Serializers, called by API View."""

from rest_framework import serializers
from template.models import NodeTemplate


class NodeTemplateSerializer(serializers.ModelSerializer):
    """Serializer for Template model."""

    class Meta:
        model = NodeTemplate
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
        ]  # Make some fields read-only
