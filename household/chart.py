from household.models import FinancialYear, HouseholdClass, HouseholdService
from collections import OrderedDict
import json


def is_range(household_class, queryset):
    """
    Check if the bill totals in each icome class are within the allocated range
    """
    filtered_queryset = []

    for income in household_class:
        for data in queryset:
            if data["household_class__name"] == income.name and data["total"]:
                if (
                    data["total"] > income.min_value
                    and data["total"] < income.max_value
                ):
                    filtered_queryset.append(data)

    return filtered_queryset


def chart_data(queryset):
    """
    Get all the household bill totals for all avaliable years and join
    the data so that plotly can draw the graph.
    Eg: for 2015/16 we need all the total for all the income levels
    """

    final_bill_totals = {}
    household_class = HouseholdClass.objects.all()

    filtered_queryset = is_range(household_class, queryset)

    for income in household_class:
        final_bill_totals[income.name] = {"x": [], "y": []}

    for value in filtered_queryset:
        final_bill_totals[value["household_class__name"]]["x"].append(
            value["financial_year__budget_year"]
        )
        final_bill_totals[value["household_class__name"]]["y"].append(
            str(value["total"])
        )

    return final_bill_totals


def stack_chart(services_queryset, bill_totals_queryset):
    """
    Function to format the household service totals data to present a stack chart
    We need to check if the bill totals for this income level are within range for a particular year,
    If so we can show the break down of the services for that year.
    
    """
    service_total_data = {}
    class_name = services_queryset[0]["household_class__name"]
    household_class = HouseholdClass.objects.filter(name=class_name)
    filtered_queryset = is_range(household_class, bill_totals_queryset)

    available_years = []
    for bills in filtered_queryset:
        if bills["household_class__name"] == class_name:
            available_years.append(bills["financial_year__budget_year"])

    services = HouseholdService.objects.all().values("name")
    for s in services:
        service_total_data[s["name"]] = {"x": [], "y": []}
    for result in services_queryset:
        if result["financial_year__budget_year"] in available_years:
            if result["total"]:
                service_total_data[result["service__name"]]["x"].append(
                    result["financial_year__budget_year"]
                )
                service_total_data[result["service__name"]]["y"].append(
                    str(result["total"])
                )
    service_total_data = OrderedDict(
        sorted(
            service_total_data.items(), key=lambda item: len(item[1]["x"]), reverse=True
        )
    )
    return json.dumps(service_total_data)


def percent_increase(queryset):
    """
    Calculate the percentage increase between the oldest financial year and the lastest financial year totals
    """
    increase_dict = {}
    household_class = HouseholdClass.objects.all()

    filtered_queryset = is_range(household_class, queryset)

    classes = {results["household_class__name"]: {} for results in filtered_queryset}
    for k, v in classes.items():
        for results in filtered_queryset:
            if results["household_class__name"] == k:
                v[results["financial_year__budget_year"]] = results["total"]
    for k, v in classes.items():
        years = list(v.keys())
        years.sort()
        start_year = years[0]
        final_year = years[-1]

        if start_year:
            percent = ((v[final_year] - v[start_year]) / v[start_year]) * 100
            if percent > 0:
                increase_dict[k] = round(percent, 2)
            else:
                increase_dict[k] = None

    increase_dict = {key.split(" ")[0]: values for key, values in increase_dict.items()}
    return increase_dict
