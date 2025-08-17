"""
Forms for managing Django Group, User, and Token models.

This module provides reusable forms for CRUD operations on
auth-related models.
"""

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
# Token
#############################################################################


class TokenForm(ObjectModelForm):
    """
    Form for managing Django REST Framework auth Tokens.

    Uses all fields from the Token model.

    Methods:
        No custom methods; uses default ObjectModelForm behavior.
    """

    class Meta:
        """
        Meta class for TokenForm.

        Attributes:
            model (Token): The DRF Token model this form operates on.
            fields (str): '__all__' to include all model fields.
        """

        model = Token
        fields = "__all__"


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
        super().__init__(*args, **kwargs)
        # Pre-populate groups if user exists
        if self.instance.pk:
            self.fields["groups"].initial = self.instance.groups.all()

    def save(self, commit=True):
        """
        Save the user instance and update the associated groups.

        Args:
            commit (bool): Whether to commit the changes to the database.

        Returns:
            User: The saved user instance.
        """
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.set(self.cleaned_data["groups"])
        return user
