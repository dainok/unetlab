"""Forms definitions for UI app."""

from django import forms
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from ui.include.forms import ObjectModelForm


#############################################################################
# Group
#############################################################################


class GroupForm(ObjectModelForm):
    """Form for the Group model."""

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), required=False, widget=forms.SelectMultiple
    )

    class Meta:
        """Meta options."""

        fields = ["name", "users"]
        model = Group

    def __init__(self, *args, **kwargs):
        """Initialize the form and pre-fill the users field for existing group instances."""
        super().__init__(*args, **kwargs)
        # Pre-populate the users field with those already in the group
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save(self, commit=True):
        """Save the group instance and update the associated users."""
        group = super().save(commit=False)
        if commit:
            group.save()
            group.user_set.set(self.cleaned_data["users"])
        return group


#############################################################################
# User
#############################################################################


class UserForm(ObjectModelForm):
    """Form for the User model."""

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=False, widget=forms.SelectMultiple
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Leave blank to not change the password."),
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Repeat password to confirm."),
    )

    class Meta:
        """Meta options."""

        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_superuser",
            "is_staff",
            "groups",
        ]

    def __init__(self, *args, **kwargs):
        """Initialize the form and pre-fill the groups field for existing users."""
        super().__init__(*args, **kwargs)
        # Pre-populate groups if user exists
        if self.instance.pk:
            self.fields["groups"].initial = self.instance.groups.all()
        if self.user and not self.user.is_superuser:
            # Disable field for non admins
            self.fields["groups"].disabled = True
            self.fields["is_staff"].disabled = True
            self.fields["is_superuser"].disabled = True

    def clean(self):
        """
        Check that password1 and password2 match.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            # if one of the two is filled in
            if password1 != password2:
                raise forms.ValidationError(_("The passwords do not match."))

        return cleaned_data

    def save(self, commit=True):
        """Save the user instance and update the associated groups."""
        obj = super().save(commit=False)

        password1 = self.cleaned_data.get("password1")
        if password1:
            # Update password only if set/modified
            obj.set_password(password1)

        if self.user and not self.user.is_superuser and obj.pk:
            # Disable field for non admins
            current_obj = User.objects.get(id=obj.id)
            obj.is_superuser = current_obj.is_superuser
            obj.is_staff = current_obj.is_staff

        if commit:
            obj.save()
            if self.user.is_superuser:
                # Set groups only if admin
                obj.groups.set(Group.objects.filter(id__in=self.cleaned_data["groups"]))

        return obj


#############################################################################
# Token
#############################################################################


class TokenForm(ObjectModelForm):
    """
    Form for the Django Token model.
    """

    class Meta:
        """Meta options."""

        fields = []
        model = Token
