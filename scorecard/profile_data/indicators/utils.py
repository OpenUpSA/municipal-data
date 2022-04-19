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


def year_month_key(result):
    return (
        result["financial_year_end.year"],
        result["financial_period.period"],
    )


def year_key(result):
    return result["financial_year_end.year"]


def item_amount_pair(item):
    return (item["item.code"], item["amount.sum"])


def collect_item_amounts(item):
    key, value = item
    return (key, dict(map(item_amount_pair, value)))


def group_items_by_year(results):
    results = groupby(results, key=year_key)
    return map(collect_item_amounts, results)


def group_items_by_month(results):
    results = groupby(results, key=year_month_key)
    return map(collect_item_amounts, results)


def sum_item_amounts(result, codes):
    return reduce(lambda r, c: r + result.get(c, 0), codes, 0)


def add_none_as_zero(a, b):
    a_non_none = 0 if a is None else a
    b_non_none = 0 if b is None else b
    return a_non_none + b_non_none


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
    year, values = item
    def f(result, key):
        print(f"result={result} key={key} year={year} values={values}")
        return (result and (values.get(key) != None))
    return reduce(
        f,
        keys,
        True
    )


def filter_for_all_keys(obj, keys):
    return filter(
        lambda item: item_has_keys(item, keys),
        obj.items()
    )


def filter_for_all_keys_versioned(obj, keys):
    result = list()
    for year, values_dict in obj.items():
        if all((k, "v2") in values_dict for k in keys):
            unversioned_dict = {k: values_dict[(k, "v2")] for k in keys}
            unversioned_dict["cube_version"] = "v2"
            result.extend([(year, unversioned_dict)])
        elif all((k, "v1") in values_dict for k in keys):
            unversioned_dict = {k: values_dict[(k, "v1")] for k in keys}
            unversioned_dict["cube_version"] = "v1"
            result.extend([(year, unversioned_dict)])
    return result


def data_source_version(year):
    if year > 2019:
        return "v2"
    else:
        return "v1"


def year_amount_key(result):
    return (
        result["financial_year_end.year"],
        result["amount.sum"],
    )


def year_assets_key(result):
    return (
        result["financial_year_end.year"],
        result["total_assets.sum"],
    )


def group_by_year(results, key="amount"):
    return map(
        lambda result: (
            result["financial_year_end.year"],
            result[f"{key}.sum"],
        ),
        results,
    )


def populate_periods(periods, years, key):
    for year, result in years:
        periods.setdefault(year, {})
        periods[year][key] = result


def group_by(items, keyfunc):
    """
    Returns dictionary of lists
    [{"a": 1}, {"b": 2}] -> {"a": [{"a": 1}], "b": [{"b": 2}]}
    """
    grouper = groupby(sorted(items, key=keyfunc), key=keyfunc)
    return dict(map(lambda g: (g[0], list(g[1])), grouper))
