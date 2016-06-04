import urllib

from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag(takes_context=True)
def table_url(context, cube, year, muni=None, items=None, amountType=None):
    if not muni:
        muni = context['geography']['this']['geo_code']

    params = {
        "year": year,
        "municipalities": muni,
    }
    if items:
        params["items"] = items
    if amountType:
        params["amountType"] = amountType

    for k, v in params.iteritems():
        if isinstance(v, list):
            params[k] = ",".join(v)

    return settings.API_BASE + "/table/" + cube + "/?" + urllib.urlencode(params)


@register.filter
def finyear(year):
    if year:
        year = int(year)
        return '%s - %s' % (year - 1, year)
    return ''
