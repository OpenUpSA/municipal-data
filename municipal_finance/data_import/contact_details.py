"""
python muni_contacts.py 'Municipal contact detail - 28 April 2016.xlsx' 'muni.csv' 'persons.csv'
"""
import csv
import pdb
import string
import sys
import traceback
import xlrd

expected_headings = [
    'Cat \nCode',
    'Locat\nCode',
    'Location \nDescription',
    'CAP',
    'Postal \nAddress 1',
    'Postal \nAddress 2',
    'Postal \nAddress 3',
    'Street \nAddress 1',
    'Street \nAddress 2',
    'Street \nAddress 3',
    'Street \nAddress 4',
    'Phone \nNumber',
    'Fax \nNumber',
    'NT \nFile No',
    'E-mail \nAddress',
    '',
    'Title',
    'Name',
    'Office\nPhone \nNumber',
    'Cell \nNumber',
    'Fax \nNumber',
    'EMAILADD',
]

expected_roles = [
    'Chief Financial Officer',
    'Conditional Grant Contacts',
    'Deputy Mayor/Executive Mayor',
    'FMG Advisor',
    'FMG Contacts',
    'FMG Interns',
    'IDP / Planning Contacts',
    'Input Form Contacts',
    'Mayor/Executive Mayor',
    'Municipal Manager',
    'Restructuring Grant Contacts',
    'Secretary of Deputy Mayor/Executive Mayor',
    'Secretary of Financial Manager',
    'Secretary of Mayor/Executive Mayor',
    'Secretary of Municipal Manager',
    'Secretary of Speaker',
    'Speaker',
]

output_roles = [
    'Chief Financial Officer',
    'Deputy Mayor/Executive Mayor',
    'Mayor/Executive Mayor',
    'Municipal Manager',
    'Secretary of Deputy Mayor/Executive Mayor',
    'Secretary of Financial Manager',
    'Secretary of Mayor/Executive Mayor',
    'Secretary of Municipal Manager',
    'Secretary of Speaker',
    'Speaker',
]

printable = set(string.printable)


def convert(workbook_name, muni_csv_name, person_csv_name):
    book = xlrd.open_workbook(workbook_name)
    sheet = book.sheet_by_index(0)
    check_columns(sheet)
    convert_persons(sheet, person_csv_name)
    convert_muni(sheet, muni_csv_name)


def convert_persons(sheet, person_csv_name):
    with open(person_csv_name, 'w') as f:
        fieldnames = [
            'demarcation_code',
            'role',
            'title',
            'name',
            'office_number',
            'fax_number',
            'email_address',
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rowx in xrange(2, sheet.nrows):
            if str(sheet.cell(rowx, 0).value) not in ['A', 'B', 'C']:
                continue
            role = sheet.cell(rowx, 15).value
            check_role(role)
            if role not in output_roles:
                continue
            item = {
                'demarcation_code': sheet.cell(rowx, 1).value,
                'role': role,
                'title': sheet.cell(rowx, 16).value,
                'name': sheet.cell(rowx, 17).value,
                'office_number': sheet.cell(rowx, 18).value,
                'fax_number': sheet.cell(rowx, 20).value,
                'email_address': sheet.cell(rowx, 21).value,
            }
            writer.writerow(item)


def convert_muni(sheet, person_csv_name):
    with open(person_csv_name, 'w') as f:
        fieldnames = [
            'demarcation_code',
            'postal_address_1',
            'postal_address_2',
            'postal_address_3',
            'street_address_1',
            'street_address_2',
            'street_address_4',
            'phone_number',
            'fax_number',
            'url',
            'street_address_3',
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        muni = None
        for rowx in xrange(2, sheet.nrows):
            if str(sheet.cell(rowx, 0).value) not in ['A', 'B', 'C']:
                continue

            # Do each muni only once
            if sheet.cell(rowx, 1).value == muni:
                continue
            else:
                muni = sheet.cell(rowx, 1).value

            item = {
                'demarcation_code': muni,
                'postal_address_1': clean(sheet.cell(rowx, 4).value),
                'postal_address_2': clean(sheet.cell(rowx, 5).value),
                'postal_address_3': clean(sheet.cell(rowx, 6).value),
                'street_address_1': clean(sheet.cell(rowx, 7).value),
                'street_address_2': clean(sheet.cell(rowx, 8).value),
                'street_address_4': clean(sheet.cell(rowx, 9).value),
                'phone_number': clean(sheet.cell(rowx, 10).value),
                'fax_number': clean(sheet.cell(rowx, 11).value),
                'url': clean(sheet.cell(rowx, 12).value),
                'street_address_3': clean(sheet.cell(rowx, 13).value),
            }
            writer.writerow(item)


def check_columns(sheet):
    for colx in xrange(0, sheet.ncols):
        heading = str(sheet.cell(1, colx).value).strip()
        if heading != expected_headings[colx]:
            raise Exception("Unexpected heading %r != %r"
                            % (heading, expected_headings[colx]))


def clean(dirty):
    return filter(lambda c: c in printable, dirty)


def check_role(role):
    if role not in expected_roles:
        raise Exception("Unexpected role %r" % role)


def main():
    [workbook_name, muni_csv_name, person_csv_name] = sys.argv[1:]
    try:
        convert(workbook_name, muni_csv_name, person_csv_name)
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)

if __name__ == "__main__":
    main()
