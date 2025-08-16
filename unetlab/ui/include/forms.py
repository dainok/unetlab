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
            visible.field.widget.attrs["class"] = "form-control"
