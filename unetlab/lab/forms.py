"""
Forms for managing Django Group, User, and Token models.

This module provides reusable forms for CRUD operations on
auth-related models.
"""

from django import forms
from django.contrib.auth.models import Group
from lab.models import Lab, LabInstance
from ui.include.forms import ObjectModelForm


#############################################################################
# Lab
#############################################################################


class LabForm(ObjectModelForm):
    shared_groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(), required=False, widget=forms.SelectMultiple
    )

    class Meta:

        model = Lab
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and pre-fill the 'groups' field for existing users.
        """
        super().__init__(*args, **kwargs)
        user = kwargs["user"]
        # Pre-populate groups if user exists
        self.fields["shared_groups"].queryset = user.groups.all()
        if self.instance.pk:
            # se sto modificando, pre-popoliamo i gruppi già associati al Lab
            self.fields["shared_groups"].initial = self.instance.shared_groups.all()


#############################################################################
# Instance
#############################################################################
class LabInstanceForm(ObjectModelForm):

    class Meta:

        model = LabInstance
        fields = "__all__"
