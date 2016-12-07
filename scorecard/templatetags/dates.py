import datetime

from django import template

register = template.Library()


@register.filter
def as_date(date_string, format=None):
    if not format:
        format = '%Y-%m-%d'

    try:
        return datetime.datetime.strptime(date_string, format)
    except ValueError as e:
        raise e
        return None
