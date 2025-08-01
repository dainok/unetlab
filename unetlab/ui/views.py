from django import forms
from django.views.generic.detail import DetailView
from crispy_forms.layout import Layout, HTML
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

class ReadOnlyDetailMixin:
    """
    Mixin per DetailView che genera un form readonly da un model,
    usando Crispy Forms e supportando `fields`, `exclude` e `field_order`.
    """
    fields = None
    exclude = None
    field_order = None

    def get_readonly_form_class(self):
        model = self.model

        class _ReadOnlyForm(forms.ModelForm):
            class Meta:
                model = self.model
                fields = self.fields or "__all__"
                exclude = self.exclude

            def __init__(self_inner, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self_inner.fields.values():
                    field.disabled = True
                self_inner.helper = FormHelper()
                self_inner.helper.form_tag = False
                layout_fields = self.field_order or list(self_inner.fields)
                self_inner.helper.layout = Layout(*layout_fields)

        return _ReadOnlyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Form = self.get_readonly_form_class()
        form = Form(instance=self.object)
        helper = FormHelper()
        helper.form_tag = False
        layout = []
        for name in form.fields.keys():
            label = form.fields[name].label or name
            value = getattr(self.object, name)
            layout.append(HTML(f'<div><strong>{label}:</strong> {value}</div>'))
        helper.layout = Layout(*layout)
        form.helper = helper
        context['form'] = form
        return context
    
class ObjectDetailView(ReadOnlyDetailMixin, DetailView):
    template_name = "objects/object_detail.html"
