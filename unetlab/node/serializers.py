"""Serializers, called by API View."""

from rest_framework import serializers
from node.models import Node, NodeTemplate


class NodeTemplateSerializer(serializers.ModelSerializer):
    """Serializer for Template model."""

    class Meta:
        model = NodeTemplate
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
        ]  # Make some fields read-only


class DiskTemplateSerializer(serializers.Serializer):
    file = serializers.FileField()


class NodeSerializer(serializers.ModelSerializer):
    """Serializer for Node model."""

    disks = DiskTemplateSerializer(read_only=True)
    template = NodeTemplateSerializer(read_only=True)

    class Meta:
        model = Node
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
        ]  # Make some fields read-only
