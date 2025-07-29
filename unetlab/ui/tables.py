import django_tables2 as tables


class GreenRedBooleanColumn(tables.TemplateColumn):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "template_name", "unetlab/tables/column_boolean_green_red.html"
        )
        super().__init__(*args, **kwargs)


class GreenRedReverseBooleanColumn(tables.TemplateColumn):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "template_name", "unetlab/tables/column_boolean_green_red_reverse.html"
        )
        super().__init__(*args, **kwargs)


class GreenBooleanColumn(tables.TemplateColumn):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("template_name", "unetlab/tables/column_boolean_green.html")
        super().__init__(*args, **kwargs)


class BooleanColumn(tables.TemplateColumn):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("template_name", "unetlab/tables/column_boolean.html")
        super().__init__(*args, **kwargs)


class SeverityColumn(tables.TemplateColumn):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("template_name", "unetlab/tables/column_severity.html")
        super().__init__(*args, **kwargs)


class SeverityAllColumn(tables.TemplateColumn):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("template_name", "unetlab/tables/column_severity_all.html")
        super().__init__(*args, **kwargs)


class URLColum(tables.TemplateColumn):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("template_name", "unetlab/tables/column_url.html")
        super().__init__(*args, **kwargs)
