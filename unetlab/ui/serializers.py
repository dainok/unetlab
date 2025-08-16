"""Serializers, called by API View."""

from django.contrib.auth.models import Group, User
from ui.include.serializers import ObjectSerializer


#############################################################################
# Group
#############################################################################


class GroupSerializer(ObjectSerializer):
    """Serializer for Log model."""

    class Meta:
        model = Group
        fields = "__all__"


#############################################################################
# User
#############################################################################


class UserSerializer(ObjectSerializer):
    """Serializer for Log model."""

    class Meta:
        model = User
        fields = "__all__"
