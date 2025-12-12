"""Forms definitions for Lab app."""

import yaml
from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from lab.models import Lab
from ui.include.forms import ObjectModelForm


#############################################################################
# Lab
#############################################################################


class LabForm(ObjectModelForm):
    """Form for the Lab model."""

    hld_yaml = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label=_("HLD (YAML)"),
        help_text=_("Insert the configuration in YAML format."),
    )
    shared_group = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        required=False,
        widget=forms.Select,
        label=_("Shared group"), help_text=_("Choose the group with whom you want to share the lab")
    )

    class Meta:

        model = Lab
        exclude = ["hld"]
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """Initialize the form and pre-fill the groups field."""
        super().__init__(*args, **kwargs)

        # Show HLD into YAML format
        if self.instance and self.instance.hld:
            self.fields["hld_yaml"].initial = yaml.safe_dump(
                self.instance.hld, sort_keys=False
            )

        # Pre-populate groups
        user = kwargs["user"]
        if user.is_superuser:
            self.fields["shared_group"].queryset = Group.objects.all()
        else:
            self.fields["shared_group"].queryset = user.groups.all()
        if self.instance.pk:
            # If lab exists, pre-populate group
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
# class LabInstanceForm(ObjectModelForm):

#     class Meta:

#         model = LabInstance
#         fields = "__all__"
