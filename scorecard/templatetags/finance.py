import urllib

from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag(takes_context=True)
def table_url(context, cube, year=None, muni=None, items=None, amountType=None):
    if not muni:
        muni = context['geography']['this']['geo_code']

    params = {
        "municipalities": muni,
    }
    if year:
        params["year"] = year
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


@register.filter
def absolute(result):
    if result is not None:
        return abs(result)


@register.filter
def month_days(n):
    # months if >= 1, else days
    if n is None:
        return None

    if n < 1.0:
        return "%d days" % (n * 30)
    else:
        return "%.2g months" % n
