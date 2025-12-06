"""Serializers for Lab app."""

from rest_framework import serializers
from lab.models import Lab
from ui.serializers import GroupSerializer

# from node.serializers import NodeSerializer


#############################################################################
# Lab
#############################################################################


class LabSerializer(serializers.ModelSerializer):
    """Serializer for Lab model."""

    class Meta:
        """Meta options."""

        model = Lab
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
        ]  # Make some fields read-only


#############################################################################
# Instance
#############################################################################


# class LabInstanceListSerializer(serializers.ModelSerializer):
#     """Serializer for Lab Instance model."""

#     class Meta:
#         """Meta options."""
#         model = LabInstance
#         fields = "__all__"
#         read_only_fields = [
#             "created_at",
#             "updated_at",
#         ]  # Make some fields read-only


# class LabInstanceDetailSerializer(serializers.ModelSerializer):
#     """Serializer for Template model."""

#     # Nested serializers
#     # groups = GroupSerializer(many=True, read_only=True)
#     lab = LabSerializer(read_only=True)
#     nodes = NodeSerializer(many=True, read_only=True)
#     # node_networks = NodeNetworkSerializer(many=True, read_only=True)

#     class Meta:
#         model = LabInstance
#         fields = "__all__"
#         read_only_fields = [
#             "created_at",
#             "updated_at",
#         ]  # Make some fields read-only
