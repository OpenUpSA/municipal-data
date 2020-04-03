from __future__ import division

import urllib
import datetime

from django import template
from django.conf import settings
from django.template.defaultfilters import floatformat

register = template.Library()


@register.simple_tag(takes_context=True)
def table_url(
    context, cube, year=None, month=None, muni=None, items=None, amountType=None
):
    if not muni:
        muni = context["geography"].geo_code

    params = {
        "municipalities": muni,
    }
    if year:
        params["year"] = year
    if month:
        params["month"] = month
    if items:
        params["items"] = items
    if amountType:
        params["amountType"] = amountType

    for k, v in params.items():
        if isinstance(v, list):
            params[k] = ",".join(v)

    return settings.API_BASE + "/table/" + cube + "/?" + urllib.parse.urlencode(params)


@register.filter
def finyear(year):
    if isinstance(year, datetime.datetime):
        date = year
        year = date.year
        if date.month >= 6:
            year -= 1

    if year:
        year = int(year)
        return "July %s - June %s" % (year - 1, year)
    return ""


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


@register.filter
def formatvalue(n, typ):
    if typ == "currency" or typ == "R":
        return u"R\u00A0" + floatformat(n, "0")

    if typ == "months":
        return month_days(n)

    if typ == "p" or typ == "percent" or typ == "%":
        return str(round(n, 2)) + "%"

    if typ == "ratio":
        return round(n, 3)

    return n


@register.inclusion_tag("profile/_comparative_list.html", takes_context=True)
def render_comparatives(context, indicator_name):
    indicator = context["indicators"][indicator_name]
    values = [v for v in indicator["values"] if v["result"] is not None]

    if values:
        date = str(values[0]["date"])
        comparisons = indicator["comparisons"].get(date)
    else:
        comparisons = None

    return {
        "comparisons": comparisons,
    }
