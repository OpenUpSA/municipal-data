"""
python audit_opinions.py directory 'audit_opinions.csv'
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
    year = re.sub(r'\d\d/', '', sheet.cell(3, 3).value)

    labels = [
        'Unauthorised Expenditure',
        'Irregular Expenditure',
        'Fruitless and Wasteful Expenditure',
    ]
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
        for rowx in xrange(9, sheet.nrows):
            if str(sheet.cell(rowx, 0).value) not in ['A', 'B', 'C']:
                continue
            for idx, label in enumerate(labels):
                item = {
                    'year': year,
                    'demarcation_code': sheet.cell(rowx, 2).value
                }
                try:
                    item['amount'] = int(round(sheet.cell(rowx, 4+idx*2).value))
                except:
                    item['amount'] = None

                item['item_label'] = label
                item['item_code'] = label_to_code[item['item_label']]
                writer.writerow(item)


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
