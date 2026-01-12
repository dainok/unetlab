"""Template tags for dynamic template behavior in Django."""

import markdown
from django import template

register = template.Library()


@register.filter
def markdownify(text):
    """Return HTML text from Markdown."""
    return markdown.markdown(text)


@register.simple_tag(takes_context=True)
def active_dropdown(context, dropdown_items):
    """Return CSS active class if current view is included in the parent dropdown menu."""
    css_class = ' active'
    request = context.get('request')
    if not request:
        return ''
    current_view = getattr(request.resolver_match, 'view_name', None)

    for dropdown_item in dropdown_items:
        if dropdown_item.get('view') == current_view:
            # If current view is included in the dropdown, return CSS
            return css_class

    return ''


@register.simple_tag(takes_context=True)
def active_view(context, view_name):
    """Return CSS active class if current view matches the given one."""
    css_class = ' active'
    request = context.get('request')
    if not request:
        return ''
    current_view = getattr(request.resolver_match, 'view_name', None)

    if current_view == view_name:
        # If current view match the requested view, return CSS
        return css_class

    return ''


@register.filter
def get_object_label(obj, field):
    """Return column name from a field name."""
    return obj._meta.get_field(field).verbose_name


@register.filter
def get_object_value(obj, field):
    """Return column value from a field name."""
    try:
        # Return 'display' value if exists
        return getattr(obj, f'get_{field}_display')()
    except AttributeError:
        pass
    return getattr(obj, field)
