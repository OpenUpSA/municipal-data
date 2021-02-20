import json

from django import template

register = template.Library()


@register.filter
def jsonify(value):
    return json.dumps(value)
