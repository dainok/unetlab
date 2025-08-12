from django import forms
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token


class ObjectModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class UserForm(ObjectModelForm):
    class Meta:
        model = User
        fields = "__all__"


class GroupForm(ObjectModelForm):
    class Meta:
        model = Group
        fields = ["name"]


class TokenForm(ObjectModelForm):
    class Meta:
        model = Token
        fields = "__all__"
