"""
Forms for managing Django Group, User, and Token models.

This module provides reusable forms for CRUD operations on
auth-related models.
"""

from django import forms
from lab.models import Lab, LabInstance
from ui.include import messages
from ui.include.forms import ObjectModelForm


#############################################################################
# Lab
#############################################################################


class LabForm(ObjectModelForm):

    class Meta:

        model = Lab
        fields = "__all__"


#############################################################################
# Instance
#############################################################################
class LabInstanceForm(ObjectModelForm):

    class Meta:

        model = LabInstance
        fields = "__all__"
