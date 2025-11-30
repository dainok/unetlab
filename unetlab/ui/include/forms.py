"""Generic reusable form definitions."""

from django import forms


class FormMixin:
    """Mixin to apply Bootstrap-friendly CSS classes to Django forms."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and apply Bootstrap CSS classes to all visible fields.
        """
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            widget_type = getattr(visible.field.widget, "input_type", None)
            css_class = ""
            if widget_type == "password":
                css_class = "form-control"
                visible.field.widget.attrs["autocomplete"] = "new-password"
            elif widget_type in ["text", "email", "password", "number"]:
                css_class = "form-control"
            elif widget_type == "checkbox":
                css_class = "form-check-input"
            elif widget_type in ["select", "selectmultiple"]:
                css_class = "form-select"
            if visible.errors:
                css_class = f"is-invalid {css_class}"
            visible.field.widget.attrs["class"] = css_class


class ObjectModelForm(FormMixin, forms.ModelForm):
    """Base ModelForm that applies Bootstrap-compatible CSS classes."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the model form and ensure Bootstrap classes are applied via FormMixin.
        """
        self.user = kwargs.pop("user", None)
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
