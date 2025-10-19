"""Serializers, called by API View."""

from rest_framework import serializers
from lab.models import Lab, LabInstance
from node.serializers import NodeSerializer


#############################################################################
# Lab
#############################################################################


class LabSerializer(serializers.ModelSerializer):
    """Serializer for Template model."""

    class Meta:
        model = Lab
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
        ]  # Make some fields read-only


#############################################################################
# Instance
#############################################################################

class LabInstanceListSerializer(serializers.ModelSerializer):
    """Serializer for Template model."""

    class Meta:
        model = LabInstance
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
        ]  # Make some fields read-only

class LabInstanceDetailSerializer(serializers.ModelSerializer):
    """Serializer for Template model."""

    # Nested serializers
    # groups = GroupSerializer(many=True, read_only=True)
    lab = LabSerializer(read_only=True)
    nodes = NodeSerializer(many=True, read_only=True)
    # node_networks = NodeNetworkSerializer(many=True, read_only=True)

    class Meta:
        model = LabInstance
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
        ]  # Make some fields read-only
