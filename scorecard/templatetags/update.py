from django import template

register = template.Library()


@register.filter
def has_updated(geo_code):
    """
    Check if a muni has beein updated
    """
    bad_list = ['KZN263', 'DC29', 'MP307', 'MP312', 'NC453']
    if geo_code in bad_list:
        return True
    return False
