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
    shared_group = forms.ModelChoiceField(
        queryset=Group.objects.all(), required=False, widget=forms.Select
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
        self.fields["shared_group"].queryset = user.groups.all()
        if self.instance.pk:
            # se sto modificando, pre-popoliamo i gruppi già associati al Lab
            self.fields["shared_group"].initial = self.instance.shared_group

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance


#############################################################################
# Instance
#############################################################################
class LabInstanceForm(ObjectModelForm):

    class Meta:

        model = LabInstance
        fields = "__all__"
