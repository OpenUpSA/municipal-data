import math

from collections import OrderedDict
from itertools import groupby
from functools import reduce


def percent(num, denom, places=2):
    if denom == 0:
        return 0
    else:
        return round(num / denom * 100, places)


def ratio(num, denom, places=2):
    if denom == 0:
        return 0
    else:
        return round(num / denom, places)


def calendar_to_financial(year, month):
    """
    2016 8 -> 2017 2
    2016 6 -> 2016 12
    2016 3 -> 2016 9
    """
    if month > 6:
        year += 1
    month = (month + 6) % 12
    if month == 0:
        month = 12
    return year, month


def quarter_idx(month):
    return ((month - 1) // 3) + 1


def quarter_tuple(year, month):
    return (year, quarter_idx(month))


def quarter_string(year, month):
    return "%sq%s" % quarter_tuple(year, month)


def generate_expected_quarter_keys(starting_key, amount):
    year, quarter = starting_key
    return map(
        lambda n: (
            (year - math.floor((n + (4 - quarter)) / 4)),
            (((((quarter - 1) - n)) % 4) + 1),
        ),
        range(amount)
    )


def quarter_index(month):
    return ((month - 1) // 3) + 1


def year_month_key(r):
    return (
        r["financial_year_end.year"],
        r["financial_period.period"],
    )


def item_amount_pair(month):
    return (month["item.code"], month["amount.sum"])


def collect_item_amounts(item):
    key, months = item
    return (key, dict(map(item_amount_pair, months)))


def group_items_by_month(results):
    results = groupby(results, key=year_month_key)
    return map(collect_item_amounts, results)


def sum_item_amounts(result, codes):
    return reduce(lambda r, c: r + result.get(c, 0), codes, 0)


def year_quarter_key(item):
    key, _ = item
    year, month = key
    return (year, quarter_index(month))


def select_latest_month(item):
    key, months = item
    sorted_months = sorted(months, key=lambda month: month[0])
    latest_month = sorted_months[-1]
    _, month_value = latest_month
    return (key, month_value)


def group_quarters(periods, select):
    quarters = groupby(
        sorted(periods, key=lambda o: o[0], reverse=True),
        key=year_quarter_key
    )
    return map(select, quarters)


def item_has_keys(item, keys):
    _, values = item
    return reduce(
        lambda result, key: (result and (values.get(key) != None)),
        keys,
        True
    )


def filter_for_all_keys(obj, keys):
    return filter(
        lambda item: item_has_keys(item, keys),
        obj.items()
    )
