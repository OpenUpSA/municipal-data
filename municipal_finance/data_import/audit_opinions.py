"""
python audit_opinions.py 'Audit opinions - 28 April 2016.xlsx' 'audit_opinions.csv'
"""
import csv
import pdb
import sys
import traceback
import xlrd


def convert(sheet, csv_file):
    book = xlrd. open_workbook(sheet)
    sheet = book.sheet_by_index(0)

    label_to_code = {
        'Adverse opinion': 'adverse',
        'Disclaimer of opinion': 'disclaimer',
        'Qualified': 'qualified',
        'Unqualified - Emphasis of Matter items': 'unqualified_emphasis_of_matter',
        'Unqualified - No findings': 'unqualified',
        'Outstanding': 'outstanding',
    }

    item = None

    with open(csv_file, 'w') as f:
        fieldnames = ['demarcation_code', 'year', 'opinion_code', 'opinion_label']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rowx in xrange(7, sheet.nrows):
            if str(sheet.cell(rowx, 0).value) not in ['A', 'B', 'C']:
                continue
            for colx in xrange(4, sheet.ncols):
                if sheet.cell(2, colx).value != '':
                    # new year
                    current_year = sheet.cell(2, colx).value
                    item = {
                        'year': current_year,
                        'demarcation_code': sheet.cell(rowx, 1).value
                    }
                val = sheet.cell(rowx, colx).value
                if val != '':
                    item['opinion_label'] = sheet.cell(4, colx).value
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
