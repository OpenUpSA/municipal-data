"""
python uif_expenditure.py "UIFW as per AGSA.xlsx" uifw.csv
"""
import csv
import pdb
import sys
import traceback
import xlrd
import re

def convert(sheet, csv_file):
    book = xlrd.open_workbook(sheet)
    sheet = book.sheet_by_index(0)

    a10th_code_to_label = {
        "9001": "Unauthorised Expenditure",
        "9002": "Irregular Expenditure",
        "9003": "Fruitless and Wasteful Expenditure",
    }

    label_to_code = {
        'Unauthorised Expenditure': 'unauthorised',
        'Irregular Expenditure': 'irregular',
        'Fruitless and Wasteful Expenditure': 'fruitless',
    }

    item = None

    with open(csv_file, 'w') as f:
        fieldnames = ['demarcation_code', 'year', 'item_code', 'item_label', 'amount']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        current_code = None
        for rowx in range(9, sheet.nrows):
            # Skip over rows without data
            if str(sheet.cell(rowx, 0).value) not in ['A', 'B', 'C']:
                continue
            # Capture the demarcation code
            demarcation_code = sheet.cell(rowx, 1).value
            # Iterate over columns with amount data
            for idx in range(0, 6):
                # Determine the current code, year and label
                code_in_head = sheet.cell(2, (4 + idx)).value
                current_code = code_in_head or current_code
                year_in_head = sheet.cell(4, (4 + idx)).value
                label = a10th_code_to_label[current_code]
                # Attempt to parse amount
                amount = sheet.cell(rowx, (4 + idx)).value
                amount = int(round(amount)) if amount else None
                # Write row to result
                writer.writerow({
                    'year': year_in_head,
                    'demarcation_code': demarcation_code,
                    'amount': amount,
                    'item_label': label,
                    'item_code': label_to_code[label],
                })

def main():
    [sheet, csv_file] = sys.argv[1:]
    try:
        convert(sheet, csv_file)
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)

if __name__ == "__main__":
    main()
