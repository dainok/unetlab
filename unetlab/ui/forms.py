"""Forms definitions for UI app."""

from django import forms
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
from ui.include import messages
from ui.include.forms import ObjectModelForm


#############################################################################
# Group
#############################################################################


class GroupForm(ObjectModelForm):
    """
    Form for the Django Group model.

    Provides a Many-to-Many field to assign users to the group.

    Attributes:
        users (ModelMultipleChoiceField): Select multiple users for the group.

    Methods:
        __init__(*args, **kwargs): Pre-populates 'users' for existing groups.
        save(commit=True): Saves the group and updates the associated users.
    """

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), required=False, widget=forms.SelectMultiple
    )

    class Meta:
        """
        Meta class for GroupForm.

        Attributes:
            model (Group): The Django Group model this form operates on.
            fields (list[str]): Fields included in the form ('name', 'users').
        """

        model = Group
        fields = ["name", "users"]

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and pre-fill the 'users' field for existing group instances.
        """
        super().__init__(*args, **kwargs)
        # Pre-populate the users field with those already in the group
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save(self, commit=True):
        """
        Save the group instance and update the associated users.

        Args:
            commit (bool): Whether to commit the changes to the database.

        Returns:
            Group: The saved group instance.
        """
        group = super().save(commit=False)
        if commit:
            group.save()
            group.user_set.set(self.cleaned_data["users"])
        return group


#############################################################################
# User
#############################################################################


class UserForm(ObjectModelForm):
    """
    Form for the Django User model.

    Provides a Many-to-Many field to assign groups to the user.

    Attributes:
        groups (ModelMultipleChoiceField): Select multiple groups for the user.

    Methods:
        __init__(*args, **kwargs): Pre-populates 'groups' for existing user instances.
        save(commit=True): Saves the user and updates the associated groups.
    """

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=False, widget=forms.SelectMultiple
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=False,
        help_text=messages.PASSWORD1_HELP,
    )

    password2 = forms.CharField(
        label="Conferma Password",
        widget=forms.PasswordInput,
        required=False,
        help_text=messages.PASSWORD2_HELP,
    )

    class Meta:
        """
        Meta class for UserForm.

        Attributes:
            model (User): The Django User model this form operates on.
            fields (list[str]): Fields included in the form:
                'username', 'first_name', 'last_name', 'email', 'is_active',
                'is_superuser', 'is_staff', 'groups'.
        """

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
        """
        Initialize the form and pre-fill the 'groups' field for existing users.
        """
        # self.user = kwargs.pop("request_user", None)
        # self.request = kwargs.pop("request", None)
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
        # user = getattr(self, "current_user", None)
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:  # if one of the two is filled in
            if password1 != password2:
                raise forms.ValidationError(messages.PASSWORD_ERROR)

        return cleaned_data

    def save(self, commit=True):
        """
        Save the user instance and update the associated groups.

        Args:
            commit (bool): Whether to commit the changes to the database.

        Returns:
            User: The saved user instance.
        """
        obj = super().save(commit=False)

        password1 = self.cleaned_data.get("password1")
        if password1:  # only if set/modified
            obj.set_password(password1)

        if self.user and not self.user.is_superuser and obj.pk:
            # Disable field for non admins
            current_obj = User.objects.get(id=obj.id)
            obj.is_superuser = current_obj.is_superuser
            obj.is_staff = current_obj.is_staff

        if commit:
            obj.save()
            # Set groups only for admins
            if self.user.is_superuser:
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
        """
        Meta class for TokenForm.
        """

        model = Token
        fields = []
