import re
import sys
import csv
import xlrd
from copy import copy

INPUT_FILE = "/Users/tomaszkolek/Downloads/buffalo.xls"
# INPUT_FILE = "/Users/tomaszkolek/Downloads/Nelson Bay.xls"
OUTPUT_BILLS = "bill.csv"
OUTPUT_INCREASE = "increase.csv"

IGNORE_COLUMN = ["Budget Year 2019/20 % incr"]
IGNORE_ROW = ["sub-total"]

CLASS_REGEX = "Monthly Account for Household - (?P<class>.*)"
INCREASE_AND_DECREASE = "% increase/-decrease"
SUB_TOTAL = "sub-total"
TOTAL_REGEX = "Total .* bill"

TOTAL = "Total"
VAT = "VAT on Services"
PERCENT_INCREASE = INCREASE_AND_DECREASE

FINANCIAL_YEAR_REGEXP = "\d+/\d+"
BUDGET_YEAR = "Budget Year (?P<financial_year>{})".format(FINANCIAL_YEAR_REGEXP)


def format_financial_year(value):
    return re.findall(FINANCIAL_YEAR_REGEXP, value)[0] or value


def get_financial_years(sheet):
    financial_years = sheet.row_slice(rowx=1, start_colx=2)
    last_financial_year = financial_years[0].value
    new_financial_years = [format_financial_year(last_financial_year)]
    for cell in financial_years[1:]:
        if not cell.value:
            cell.value = last_financial_year
        else:
            last_financial_year = cell.value

        new_financial_years.append(format_financial_year(cell.value))

    return new_financial_years


def get_budget_phases(sheet):
    budget_phases = sheet.row_slice(rowx=2, start_colx=2)
    return [cell.value for cell in budget_phases]


def get_class(value):
    match = re.match(CLASS_REGEX, value)
    if match:
        return match.group("class")


def get_services_start_indexes(sheet):
    first_column = sheet.col_values(0)
    result = []
    for index, col_value in enumerate(first_column):
        class_name = get_class(col_value)
        if class_name:
            result.append((class_name, index))

    return result


def get_service_name(cell_value):
    match = re.match(TOTAL_REGEX, cell_value)
    return TOTAL if match else cell_value


def get_services_in_details(sheet, start_index, end_index):
    result = {}
    should_exit = False
    for row_number in range(start_index, end_index):
        row = sheet.row_slice(rowx=row_number)
        for index, cell in enumerate(row):
            if index == 0:
                service_name = get_service_name(cell.value)
                result[service_name] = []
            elif index > 1:
                result[service_name].append(cell.value)

            if cell.value == INCREASE_AND_DECREASE:
                should_exit = True

        if should_exit:
            return result


def get_info(sheet, services_indexes):
    result = {}
    current_class_name, current_index = services_indexes[0]
    for next_class_name, next_index in services_indexes[1:]:
        result[current_class_name] = get_services_in_details(sheet, current_index + 2, next_index)
        current_index = next_index
        current_class_name = next_class_name

    result[current_class_name] = get_services_in_details(sheet, current_index + 2, sheet.nrows)
    return result


def get_list_from_financial_year_and_budget_phase(financial_year, budget_phase):
    match = re.match(BUDGET_YEAR, budget_phase)
    if match:
        return [match.group("financial_year"), "Budget Year"]

    return [financial_year, budget_phase]


def get_household_increase_lists(results, financial_years, budget_phases):
    headers = ["Financial Year", "Budget Phase", "Class", "Total", "Vat", "Percent Increase"]
    csv_lines = [headers]
    for index in range(len(financial_years)):
        if budget_phases[index] in IGNORE_COLUMN:
            continue

        base_elem = get_list_from_financial_year_and_budget_phase(financial_years[index], budget_phases[index])
        for class_name, details in results.items():
            elem = copy(base_elem)
            elem += [class_name, details[TOTAL][index], details[VAT][index], details[PERCENT_INCREASE][index]]
            csv_lines.append(elem)

    return csv_lines


def get_household_bills_lists(results, financial_years, budget_phases):
    headers = ["Financial Year", "Budget Phase", "Class", "Service Name", "Total"]
    csv_lines = [headers]
    for index in range(len(financial_years)):
        if budget_phases[index] in IGNORE_COLUMN:
            continue

        base_elem = get_list_from_financial_year_and_budget_phase(financial_years[index], budget_phases[index])
        for class_name, details in results.items():
            elem_with_class_name = base_elem + [class_name]
            for service_name, value in details.items():
                if service_name not in [TOTAL, VAT, PERCENT_INCREASE, SUB_TOTAL]:
                    elem_with_service_name = elem_with_class_name + [service_name, value[index]]
                    csv_lines.append(elem_with_service_name)

    return csv_lines


def create_csv(lines, output):
    with open(output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for line in lines:
            writer.writerow(line)


def main(input_file, increase_output, bills_output):
    book = xlrd.open_workbook(input_file, formatting_info=True)
    sheet = book.sheet_by_index(0)

    financial_years = get_financial_years(sheet)
    budget_phases = get_budget_phases(sheet)
    services_indexes = get_services_start_indexes(sheet)
    results = get_info(sheet, services_indexes)
    household_increase_lists = get_household_increase_lists(results, financial_years, budget_phases)
    household_bills_lists = get_household_bills_lists(results, financial_years, budget_phases)

    create_csv(household_increase_lists, increase_output)
    create_csv(household_bills_lists, bills_output)


if __name__ == "__main__":
    input_file = sys.argv[1]
    increase_output = sys.argv[2]
    bills_output = sys.argv[3]
    # input_file = INPUT_FILE
    # increase_output = OUTPUT_INCREASE
    # bills_output = OUTPUT_BILLS
    main(input_file, increase_output, bills_output)
