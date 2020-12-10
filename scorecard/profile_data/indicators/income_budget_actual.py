from .indicator_calculator import IndicatorCalculator
from itertools import groupby
from .utils import year_key
from functools import reduce
import re
from collections import defaultdict


def group_by(items, key):
    """Returns dictionary of lists"""
    grouper = groupby(sorted(items, key=key), key=key)
    return dict(map(lambda g: (g[0], list(g[1])), grouper))


class IncomeTimeSeries(IndicatorCalculator):
    name = "income_time_series"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
