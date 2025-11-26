"""Template tags for dynamic template behavior in Django."""

from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()


# @register.simple_tag
# def get_verbose_field_name(instance, field_name):
#     """
#     Ritorna il verbose_name del campo `field_name` sull’istanza `instance`.
#     """
#     return instance._meta.get_field(field_name).verbose_name

@register.filter
def get(value, arg):
    """
    Restituisce value[arg] se è un dict,
    oppure getattr(value, arg) se è un oggetto.
    """
    if value is None:
        return None
    if isinstance(value, dict):
        return value.get(arg)
    return getattr(value, arg, None)

@register.simple_tag(takes_context=True)
def is_active(context, *view_names):
    """Determine if the current view matches any of the given view names.

    Args:
        context (dict): Template context, must contain 'request'.
        *view_names (str): One or more view names to compare with the current view.

    Returns:
        str: " active" if the current view matches any view_name, otherwise an empty string.
    """
    request = context.get("request")
    if not request:
        return ""
    current_view = getattr(request.resolver_match, "view_name", None)
    if current_view in view_names:
        return " active"
    return ""

# @register.simple_tag
# def exist_view(view_name, *args, **kwargs):
#     """
#     Ritorna True se il nome di view esiste (cioè se reverse() funziona),
#     altrimenti False.
#     """
#     try:
#         reverse(view_name, args=args, kwargs=kwargs)
#         return True
#     except NoReverseMatch:
#         return False
    