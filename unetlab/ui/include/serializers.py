"""Serializers, called by API View."""

from rest_framework import serializers

class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = "__all__"
