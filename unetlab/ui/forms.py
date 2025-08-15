from django import forms
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
from ui.include.forms import ObjectModelForm


class UserForm(ObjectModelForm):
    class Meta:
        model = User
        fields = "__all__"


class GroupForm(ObjectModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple
    )

    class Meta:
        model = Group
        fields = ["name", "users"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Precompila il campo users con quelli già nel gruppo
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
            group.user_set.set(self.cleaned_data["users"])
        return group



class TokenForm(ObjectModelForm):
    class Meta:
        model = Token
        fields = "__all__"

