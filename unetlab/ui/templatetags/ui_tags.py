"""Template tags for dynamic template behavior in Django."""

from django import template

register = template.Library()


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
