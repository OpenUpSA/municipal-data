# based on json_script in Django 2.1

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def json_script_escape(json_string, not_in_an_attr=False):
    """
    Escape all the HTML/XML special characters with their unicode escapes, so
    value is safe to be output anywhere !!EXCEPT!! for inside a tag attribute.
    """
    if not not_in_an_attr:
        raise Exception(
            "This is intended to be used in a tag body, not a tag attribute!"
        )

    json_string = json_string.replace(">", "\\u003E")
    json_string = json_string.replace("<", "\\u003C")
    json_string = json_string.replace("&", "\\u0026")
    return mark_safe(json_string)
