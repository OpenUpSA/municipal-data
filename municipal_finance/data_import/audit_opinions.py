"""
python audit_opinions.py 'Audit opinions - 28 April 2016.xlsx' 'audit_opinions.csv'
"""
import csv
import pdb
import sys
import traceback
import xlrd


def convert(sheet, csv_file):
    book = xlrd.open_workbook(sheet)
    sheet = book.sheet_by_index(0)

    label_to_code = {
        'Adverse opinion': 'adverse',
        'Disclaimer of opinion': 'disclaimer',
        'Qualified': 'qualified',
        'Unqualified - Emphasis of Matter items': 'unqualified_emphasis_of_matter',
        'Unqualified - With findings': 'unqualified_emphasis_of_matter',
        'Unqualified - No findings': 'unqualified',
        'Outstanding': 'outstanding',
    }
    label_normalised = {
        'Adverse opinion': 'Adverse opinion',
        'Disclaimer of opinion': 'Disclaimer of opinion',
        'Qualified': 'Qualified',
        'Unqualified - Emphasis of Matter items': 'Unqualified - Emphasis of Matter items',
        'Unqualified - With findings': 'Unqualified - Emphasis of Matter items',
        'Unqualified - No findings': 'Unqualified - No findings',
        'Outstanding': 'Outstanding',
    }

    item = None

    with open(csv_file, 'w') as f:
        fieldnames = ['demarcation_code', 'year', 'opinion_code', 'opinion_label']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rowx in range(7, sheet.nrows):
            if sheet.cell(rowx, 0).value == 'TOTAL':
                continue
            for colx in range(4, sheet.ncols):
                if sheet.cell(3, colx).value != '':
                    # new year
                    current_year = int(sheet.cell(3, colx).value)
                    item = {
                        'year': current_year,
                        'demarcation_code': sheet.cell(rowx, 1).value
                    }
                val = sheet.cell(rowx, colx).value
                if val != '':
                    item['opinion_label'] = label_normalised[sheet.cell(rowx, colx).value]
                    item['opinion_code'] = label_to_code[item['opinion_label']]
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
