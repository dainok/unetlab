from django import forms
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
from ui.include.forms import ObjectModelForm


#############################################################################
# Group
#############################################################################


class GroupForm(ObjectModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), required=False, widget=forms.SelectMultiple
    )

    class Meta:
        model = Group
        fields = ["name", "users"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate the users field with those already in the group
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
            group.user_set.set(self.cleaned_data["users"])
        return group


#############################################################################
# Token
#############################################################################


class TokenForm(ObjectModelForm):
    class Meta:
        model = Token
        fields = "__all__"


#############################################################################
# User
#############################################################################


class UserForm(ObjectModelForm):
    class Meta:
        model = User
        fields = "__all__"
