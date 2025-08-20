"""
Forms for managing Django Group, User, and Token models.

This module provides reusable forms for CRUD operations on
auth-related models.
"""

from repository.models import Repository
from ui.include.forms import ObjectModelForm


class RepositoryForm(ObjectModelForm):
    """
    Form for the Django Repository model.

    Provides a Many-to-Many field to assign users to the group.

    Attributes:
        users (ModelMultipleChoiceField): Select multiple users for the group.

    Methods:
        __init__(*args, **kwargs): Pre-populates 'users' for existing groups.
        save(commit=True): Saves the group and updates the associated users.
    """

    # users = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.all(), required=False, widget=forms.SelectMultiple
    # )

    class Meta:
        """
        Meta class for GroupForm.

        Attributes:
            model (Group): The Django Group model this form operates on.
            fields (list[str]): Fields included in the form ('name', 'users').
        """

        model = Repository
        fields = "__all__"
