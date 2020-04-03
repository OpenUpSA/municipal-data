"""
Script to format household data into flat csv file.
"""
import time
import csv
import pandas

service_totals = pandas.DataFrame(
    columns=[
        "Geography",
        "Financial Year",
        "Budget Phase",
        "Class",
        "Service Name",
        "Total",
    ]
)

bill_totals = pandas.DataFrame(
    columns=[
        "Geography",
        "Financial Year",
        "Budget Phase",
        "Class",
        "Total",
        "Percent Increase",
    ]
)

col = {
    "a": {"y": "2015/16", "b": "Audited Outcome", "r": "2015/16 AUD"},
    "b": {"y": "2016/17", "b": "Audited Outcome", "r": "2016/17 AUD"},
    "c": {"y": "2017/18", "b": "Audited Outcome", "r": "2017/18 AUD"},
    "d": {"y": "2018/19", "b": "Original Budget", "r": "2018/19 OB"},
    "e": {"y": "2018/19", "b": "Adjusted Budget", "r": "2018/19 AB"},
    "f": {"y": "2019/20", "b": "Budget Year", "r": "2019/20 BY"},
    "g": {"y": "2020/21", "b": "Budget Year", "r": "2020/21 BY"},
    "h": {"y": "2021/22", "b": "Budget Year", "r": "2021/22 BY"},
}


def clean(values):
    """
    Clean up the value
    convert (100) to -100
    """
    if "(" in values:
        values = "-" + values.replace("(", "").replace(")", "")

    values = values.replace(",", "")
    try:
        return float(values)
    except ValueError:
        return values


with open("national_household_data.csv") as house_csv:
    reader = csv.DictReader(house_csv)
    household_class = ""
    count = 1
    for row in reader:
        if row["Description"] == "Monthly Account for Household - Middle Income Range":
            print("Working with Middle Income Range")
            household_class = "Middle Income Range"
            continue
        elif row["Description"] == "Monthly Account for Household - Affordable Range":
            print("Working with  Affordable Range")
            household_class = "Affordable Range"
            continue
        elif (
            row["Description"]
            == "Monthly Account for Household - Indigent HH receiving FBS"
        ):
            print("Working with  Indigent Range")
            household_class = "Indigent HH receiving FBS"
            continue
        if row["Description"] == "Rates and services charges:":
            continue
        if row["Description"] == "sub-total":
            continue
        if row["Description"] == "VAT on Services":
            continue

        if row["Description"] == "Total large household bill:":
            for k, v in col.items():

                bill_totals.loc[count] = [
                    row["Code"],
                    v["y"],
                    v["b"],
                    household_class,
                    clean(row[v["r"]]),
                    "",
                ]
                count += 1
        if row["Description"] == "% increase/-decrease":
            for k, v in col.items():

                search_row = bill_totals.loc[
                    (bill_totals["Geography"] == row["Code"])
                    & (bill_totals["Financial Year"] == v["y"])
                    & (bill_totals["Budget Phase"] == v["b"])
                    & (bill_totals["Class"] == household_class)
                ]
                if not search_row.empty:
                    bill_totals.at[search_row.index[0], "Percent Increase"] = clean(
                        row[v["r"]]
                    )

        if row["Description"] in [
            "Property rates",
            "Electricity: Basic levy",
            "Electricity: Consumption",
            "Water: Basic levy",
            "Water: Consumption",
            "Sanitation",
            "Refuse removal",
            "Other",
        ]:
            for k, v in col.items():
                service_totals.loc[count] = [
                    row["Code"],
                    v["y"],
                    v["b"],
                    household_class,
                    row["Description"],
                    clean(row[v["r"]]),
                ]
                count += 1

    bill_totals.to_csv("national_bill_totals.csv", index=False)
    service_totals.to_csv("national_service_totals.csv", index=False)
