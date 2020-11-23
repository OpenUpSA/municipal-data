
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
