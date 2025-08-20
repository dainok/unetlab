"""Serializers, called by API View."""

from rest_framework import serializers
from repository.models import Repository


class RepositorySerializer(serializers.ModelSerializer):
    """Serializer for Repository model."""

    class Meta:
        model = Repository
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
        ]
