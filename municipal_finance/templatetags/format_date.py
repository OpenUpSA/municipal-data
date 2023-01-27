import dateutil
from django import template

register = template.Library()


@register.filter
def format_date(value):
    date = dateutil.parser.parse(value)
    return str(date)
