"""
Forms for managing Django Group, User, and Token models.

This module provides reusable forms for CRUD operations on
auth-related models.
"""

import yaml
from django import forms
from django.contrib.auth.models import Group
from lab.models import Lab, LabInstance
from ui.include.forms import ObjectModelForm


#############################################################################
# Lab
#############################################################################


class LabForm(ObjectModelForm):
    hld_yaml = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="HLD (YAML)",
        help_text="Inserisci la configurazione in YAML",
    )
    shared_group = forms.ModelChoiceField(
        queryset=Group.objects.all(), required=False, widget=forms.Select
    )

    class Meta:

        model = Lab
        exclude = ["hld"]
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and pre-fill the 'groups' field for existing users.
        """
        super().__init__(*args, **kwargs)

        # Mostra il contenuto JSON come YAML
        if self.instance and self.instance.hld:
            self.fields["hld_yaml"].initial = yaml.safe_dump(
                self.instance.hld, sort_keys=False
            )

        user = kwargs["user"]
        # Pre-populate groups if user exists
        self.fields["shared_group"].queryset = user.groups.all()
        if self.instance.pk:
            # se sto modificando, pre-popoliamo i gruppi già associati al Lab
            self.fields["shared_group"].initial = self.instance.shared_group

    def clean_hld_yaml(self):
        data = self.cleaned_data["hld_yaml"]
        try:
            parsed = yaml.safe_load(data) if data else {}
        except yaml.YAMLError as e:
            raise forms.ValidationError(f"Errore YAML: {e}")
        return parsed

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.hld = self.cleaned_data["hld_yaml"]

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
