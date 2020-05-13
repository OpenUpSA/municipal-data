from metro.models import IndicatorQuarterResult
from django import template

register = template.Library()


@register.filter(name="percentage")
def percentage(value, arg):
    """
    convert quarterly value into percentage
    """
    if not value:
        return 0
    if not arg:
        return 0
    if "%" in value:
        return float(value.replace("%", ""))
    else:
        result = (
            IndicatorQuarterResult.clean_value(value)
            / IndicatorQuarterResult.clean_value(arg)
        ) * 100
        return int(result)
