"""Serializers for Group and User models.

These serializers are used by the API views to convert model
instances to and from JSON representations.
"""

from django.contrib.auth.models import Group, User
from ui.include.serializers import ObjectSerializer


#############################################################################
# Group
#############################################################################


class GroupSerializer(ObjectSerializer):
    """Serializer for the `Group` model."""

    class Meta:
        model = Group
        fields = "__all__"


#############################################################################
# User
#############################################################################


class UserSerializer(ObjectSerializer):
    """Serializer for the `User` model."""

    class Meta:
        model = User
        fields = "__all__"
