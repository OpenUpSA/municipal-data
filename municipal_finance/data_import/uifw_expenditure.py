"""
python uif_expenditure.py "UIFW as per AGSA.xlsx" uifw.csv
"""
import csv
import pdb
import sys
import traceback
import xlrd


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
        for rowx in range(7, sheet.nrows):
            if str(sheet.cell(rowx, 0).value) not in ['A', 'B', 'C']:
                continue
            for year_col in [6, 7, 8]:
                item = {
                    'year': sheet.cell(2, year_col).value,
                    'demarcation_code': sheet.cell(rowx, 1).value
                }
                try:
                    item['amount'] = int(round(sheet.cell(rowx, year_col).value))
                except:
                    item['amount'] = None

                item['item_label'] = a10th_code_to_label[sheet.cell(rowx, 4).value]
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
