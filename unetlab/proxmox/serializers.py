"""Serializers, called by API View."""

from rest_framework import serializers
from proxmox.models import ProxmoxHost


class ProxmoxHostSerializer(serializers.ModelSerializer):
    """Serializer for ProxmoxHost model."""

    class Meta:
        model = ProxmoxHost
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
