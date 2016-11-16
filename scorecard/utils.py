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
