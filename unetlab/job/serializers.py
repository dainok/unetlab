"""Serializers, called by API View."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from rest_framework import serializers
from job.models import Job


class JobSerializer(serializers.ModelSerializer):
    """Serialize job."""

    # logs = LogSerializer(many=True, read_only=True)

    class Meta:
        """Serializer metadata."""

        model = Job
        fields = ["id", "user", "status", "created_at"]
        # fields = ['id', 'user', 'status', 'logs', 'created_at']
