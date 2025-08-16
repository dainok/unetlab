"""Generic serializer for REST API views.

Provides a base serializer that can be inherited by model-specific serializers.
"""

from rest_framework import serializers


class ObjectSerializer(serializers.ModelSerializer):
    """Base serializer for Django models.

    Inherit from this class to create a serializer for any model.

    Attributes:
        Meta.model: Should be set in subclasses to the target model.
        Meta.fields: Set to "__all__" to include all fields by default.
    """

    class Meta:
        """Meta options for the serializer.

        Attributes:
            model (django.db.models.Model): Target model for the serializer. Must be overridden.
            fields (str or list): Fields to include. "__all__" includes all fields of the model.
        """

        model = None
        fields = "__all__"
