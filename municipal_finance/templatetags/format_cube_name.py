import dateutil
from django import template

register = template.Library()

@register.filter
def format_cube_name(value):
    return value.replace("_", " ")
