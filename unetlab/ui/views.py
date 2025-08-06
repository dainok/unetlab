from typing import Any
from django import forms
from django.views.generic.detail import DetailView
from django.utils.module_loading import import_string
from django_tables2.columns import Column
from django_tables2 import TemplateColumn
from django.template import Template, Context


class ObjectDetailView(DetailView):
    exclude = []
    sequence = []
    attrs = {
        "title": "",
        "description": ""
    }
    template_name = "objects/object_detail.html"
    list_view = None

    def get_list_view(self):
        if self.list_view is not None:
            return self.list_view
        # Se non definito, calcola da model
        return f"{self.model._meta.model_name}_list"

    def get_column_fields(self):
        """
        Restituisce gli attributi della classe che sono istanze di django_tables2 Column.
        """
        return {
            attr_name: getattr(self.__class__, attr_name)
            for attr_name in dir(self.__class__)
            if isinstance(getattr(self.__class__, attr_name), Column)
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        fields = obj._meta.fields

        column_fields = self.get_column_fields()
        data = {}

        for field in fields:
            field_name = field.name
            if field_name in self.exclude:
                continue

            value = getattr(obj, field_name)
            # column = column_fields.get(field_name)

            # if isinstance(column, TemplateColumn):
            #     template = Template(column.template_code)
            #     ctx = Context({"record": obj, "value": value})
            #     value = template.render(ctx)
            # Altri tipi di colonne possono essere gestiti qui se vuoi

            data[field_name] = value

        # Ordina secondo sequence, se presente
        if self.sequence:
            ordered_data = {k: data[k] for k in self.sequence if k in data}
            for k in data:
                if k not in ordered_data:
                    ordered_data[k] = data[k]
            data = ordered_data


        context["object"] = data
        context["attrs"] = {
            "title": self.attrs.get("title", ""),
            "description": self.attrs.get("description", ""),
        }
        context["list_view"] = self.get_list_view()
        return context