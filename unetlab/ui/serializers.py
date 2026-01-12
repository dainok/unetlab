"""Serializers for UI app."""

from django.contrib.auth.models import Group, User
from rest_framework import serializers
from ui.include.serializers import ObjectSerializer


#############################################################################
# Group
#############################################################################


class GroupSerializer(ObjectSerializer):
    """Serializer for the Group model."""

    class Meta:
        """Meta options."""

        fields = ('id', 'name')
        model = Group


#############################################################################
# User
#############################################################################


class UserSerializer(ObjectSerializer):
    """Serializer for the User model."""

    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        required=False,
        default=[],
    )
    groups_display = serializers.SerializerMethodField()

    class Meta:
        """Meta options."""

        model = User
        fields = (
            'date_joined',
            'email',
            'first_name',
            'groups_display',
            'groups',
            'id',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'last_name',
            'username',
        )
        read_only_fields = (
            'date_joined',
            'groups_display',
            'id',
            'last_login',
        )

    def get_groups_display(self, obj) -> list:
        """Return Group names in readable format."""
        return [
            {'id': group.id, 'name': group.name}
            for group in obj.groups.all().order_by('name')
        ]

    def update(self, instance, validated_data) -> User:
        """Update the User objects managing password and Groups."""
        groups = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            # Update standard fields
            setattr(instance, attr, value)

        # Update (overwrite) Groups
        if groups is not None:
            instance.groups.set(groups)

        if password:
            # Update password if set
            instance.set_password(password)

        instance.save()
        return instance

    def get_fields(self) -> dict:
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and request.user and not request.user.is_superuser:
            # Web request -> disable field for non admins
            fields['groups'].read_only = True
            fields['is_staff'].read_only = True
            fields['is_superuser'].read_only = True
        return fields
