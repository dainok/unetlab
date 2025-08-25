"""Generic reusable form definitions."""

from django import forms


class FormMixin:
    """
    Mixin to apply Bootstrap-friendly CSS classes to Django forms.

    When included in a Form or ModelForm, this mixin automatically
    iterates over all visible fields and applies appropriate CSS classes
    to match Bootstrap's form styles.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and apply Bootstrap CSS classes
        to all visible fields.
        """
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            widget_type = getattr(visible.field.widget, "input_type", None)
            if widget_type == "password":
                visible.field.widget.attrs["class"] = "form-control"
                visible.field.widget.attrs["autocomplete"] = "new-password"
            elif widget_type in ["text", "email", "password", "number"]:
                visible.field.widget.attrs["class"] = "form-control"
            elif widget_type == "checkbox":
                visible.field.widget.attrs["class"] = "form-check-input"
            elif widget_type in ["select", "selectmultiple"]:
                visible.field.widget.attrs["class"] = "form-select"


class ObjectModelForm(FormMixin, forms.ModelForm):
    """Base ModelForm that applies Bootstrap-compatible CSS classes.

    All visible fields will automatically receive the CSS class
    `"form-control"` to ensure consistent styling across forms.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the model form and ensure Bootstrap classes are applied
        via FormMixin.
        """
        self.user = kwargs.pop("user", None)  # Extract and save user
        super().__init__(*args, **kwargs)
