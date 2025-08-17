"""Generic reusable form definitions."""

from django import forms


class ObjectModelForm(forms.ModelForm):
    """Base ModelForm that applies Bootstrap-compatible CSS classes.

    All visible fields will automatically receive the CSS class
    `"form-control"` to ensure consistent styling across forms.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the form and apply CSS classes to visible fields."""
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            widget_type = getattr(visible.field.widget, "input_type", None)
            if widget_type in ["text", "email", "password", "number"]:
                visible.field.widget.attrs["class"] = "form-control"
            elif widget_type == "checkbox":
                visible.field.widget.attrs["class"] = "form-check-input"
            elif widget_type in ["select", "selectmultiple"]:
                visible.field.widget.attrs["class"] = "form-select"
