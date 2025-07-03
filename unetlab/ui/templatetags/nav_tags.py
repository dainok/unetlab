from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active(context, *view_names):
    """Return " active" if the current view is in input list."""
    request = context.get("request")
    if not request:
        return ""
    current_view = getattr(request.resolver_match, "view_name", None)
    if current_view in view_names:
        return " active"
    return ""
