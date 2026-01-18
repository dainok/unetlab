"""Serializers for Task app."""

from rest_framework import serializers
from task.models import Task, Log


class LogSerializer(serializers.ModelSerializer):
    """Serializer for Log model."""

    class Meta:
        model = Log
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]  # Make some fields read-only


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Job model.

    Include related logs as nested representation in read-only mode.
    """

    logs = LogSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]  # Make some fields read-only
