from __future__ import division

import urllib
import datetime

from django import template
from django.conf import settings
from django.template.defaultfilters import floatformat

register = template.Library()


@register.simple_tag(takes_context=True)
def table_url(context, cube, year=None, month=None, muni=None, items=None, amountType=None):
    if not muni:
        muni = context['geography'].geo_code

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

    for k, v in params.iteritems():
        if isinstance(v, list):
            params[k] = ",".join(v)

    return settings.API_BASE + "/table/" + cube + "/?" + urllib.urlencode(params)


@register.filter
def finyear(year):
    if isinstance(year, datetime.datetime):
        date = year
        year = date.year
        if date.month >= 6:
            year -= 1

    if year:
        year = int(year)
        return 'July %s - June %s' % (year - 1, year)
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


@register.filter
def formatvalue(n, typ):
    if typ == 'currency' or typ == 'R':
        return u"R\u00A0" + floatformat(n, "0")

    if typ == 'months':
        return month_days(n)

    if typ == 'p' or typ == 'percent' or typ == '%':
        return str(n) + '%'

    if typ == 'ratio':
        return n

    return n


@register.inclusion_tag('profile/_comparative_list.html', takes_context=True)
def render_comparatives(context, indicator_name):
    indicator = context['indicators'][indicator_name]
    values = [v for v in indicator['values'] if v['result'] is not None]

    if values:
        date = str(values[0]['date'])
        comparisons = indicator['comparisons'].get(date)
    else:
        comparisons = None

    return {
        'comparisons': comparisons,
    }

dummy_lookup = {
    "employment_by_race" : {
        "heading" : "Employment by race",
        "description" : "Employment figures in 2016 for 15 to 64-year-olds.",
        "comparative" : "employment rate",
        "indicator" : "employed_by_race",
    },
    "unemployment_by_race" : {
        "heading" : "Unemployment by race",
        "description" : "Unemployment figures in 2016 for 15 to 64-year-olds.",
        "comparative" : "unemployment rate",
        "indicator" : "unemployment_by_race",
    },
    "lighting_by_electricity" : {
        "heading" : "Lighting using electricity",
        "period" : "2013 - 2016",
        "description" : "The number of households that use electricity for lighting.",
        "comparative" : "number of households using electricity",
        "indicator" : "lighting_by_electricity",
	"indicator_comparatives" : "&nbsp;",
        "comparison_description" : 'Since 2013, the number of households with electricity has increased by 43%, more than 1.5 times the national average <em>(these figures are for demonstration purposes only)</em>',
    },
    "lighting_by_paraffin" : {
        "heading" : "Lighting using paraffin",
        "period" : "2013 - 2016",
        "description" : "The number of households that use paraffin for lighting.",
        "comparative" : "number of households using paraffin",
        "indicator" : "lighting_by_paraffin",
	"indicator_comparatives" : "&nbsp;",
        "comparison_description" : 'Since 2013, the number of households using paraffin has decreased by 10%, about 90% of the national average <em>(these figures are for demonstration purposes only)</em>',
    },
    "non_current_liabilities" : {
        "heading" : "Non-current liabilities",
        "period" : "2013 - 2016",
        "description" : "",
        "comparative" : "unemployment rate",
        "indicator" : "non_current_liabilities",
        "indicator_comparatives" : "&nbsp;",
        "comparison_description" : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    },
    "current_liabilities" : {
        "heading" : "Current liabilities",
        "period" : "2013 - 2016",
        "description" : "",
        "comparative" : "unemployment rate",
        "indicator" : "current_liabilities",
        "indicator_comparatives" : "&nbsp;",
        "comparison_description" : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    },
    "total_income" : {
        "heading" : "Total income",
        "period" : "2013 - 2016",
        "description" : "",
        "comparative" : "unemployment rate",
        "indicator" : "total_income",
        "indicator_comparatives" : "&nbsp;",
        "comparison_description" : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    },
    "total_expenditure" : {
        "heading" : "Total expenditure",
        "period" : "2013 - 2016",
        "description" : "",
        "comparative" : "unemployment rate",
        "indicator" : "total_expenditure",
        "indicator_comparatives" : "&nbsp;",
        "comparison_description" : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    },
}

@register.inclusion_tag('profile/dummy.html', takes_context=True)
def render_dummy(context, indicator_name):
    return dummy_lookup[indicator_name]
