"""
python muni_contacts.py 'Municipal contact detail - 28 April 2016.xlsx' 'muni.csv' 'persons.csv'
"""
import csv
import pdb
import string
import sys
import traceback
import xlrd
from urlparse import urlparse

expected_headings = [
    'Location Description',
    'Locat Code',
    'CAP',
    'Postal Address 1',
    'Postal Address 2',
    'Postal Address 3',
    'Street Address 1',
    'Street Address 2',
    'Street Address 3',
    'Street Address 4',
    'Phone Number',
    'Fax Number',
    'NT File No',
    'E-mail Address',
    '',
    'Title',
    'Name',
    'Phone Number',
    'Cell Number',
    'Fax Number',
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
    with open(person_csv_name, 'wb') as f:
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
        for rowx in xrange(1, sheet.nrows):
            if str(sheet.cell(rowx, 2).value) not in ['H', 'L', 'M']:
                continue
            role = sheet.cell(rowx, 14).value
            check_role(role)
            if role not in output_roles:
                continue
            item = {
                'demarcation_code': sheet.cell(rowx, 1).value.encode('utf-8'),
                'role': role.encode('utf-8'),
                'title': sheet.cell(rowx, 15).value.encode('utf-8'),
                'name': clean(sheet.cell(rowx, 16)).encode('utf-8'),
                'office_number': sheet.cell(rowx, 17).value.encode('utf-8'),
                'fax_number': sheet.cell(rowx, 19).value.encode('utf-8'),
                'email_address': sheet.cell(rowx, 20).value.encode('utf-8'),
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
            'street_address_3',
            'street_address_4',
            'phone_number',
            'fax_number',
            'url',
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        muni = None
        for rowx in xrange(1, sheet.nrows):
            if str(sheet.cell(rowx, 2).value) not in ['H', 'L', 'M']:
                continue

            # Do each muni only once
            if sheet.cell(rowx, 1).value == muni:
                continue
            else:
                muni = sheet.cell(rowx, 1).value

            item = {
                'demarcation_code': muni,
                'postal_address_1': clean(sheet.cell(rowx, 3)),
                'postal_address_2': clean_address(sheet.cell(rowx, 4)),
                'postal_address_3': clean_address(sheet.cell(rowx, 5)),
                'street_address_1': clean(sheet.cell(rowx, 6)),
                'street_address_2': clean_address(sheet.cell(rowx, 7)),
                'street_address_3': clean_address(sheet.cell(rowx, 8)),
                'street_address_4': clean_address(sheet.cell(rowx, 9)),
                'phone_number': clean(sheet.cell(rowx, 10)),
                'fax_number': clean(sheet.cell(rowx, 11)),
                'url': clean_url(sheet.cell(rowx, 13).value),
            }
            writer.writerow(item)


def check_columns(sheet):
    for colx in xrange(0, sheet.ncols):
        heading = str(sheet.cell(0, colx).value).strip()
        if heading != expected_headings[colx]:
            raise Exception("Unexpected heading %r != %r <- expected"
                            % (heading, expected_headings[colx]))


def clean(dirty):
    if dirty.ctype == 2:
        return str(int(dirty.value))
    else:
        return filter(lambda c: c in printable, dirty.value)


def clean_address(dirty):
    """zero-pad if it looks like 4-digit post codes"""
    if dirty.ctype == 2:
        return format(int(dirty.value), '04')
    else:
        return filter(lambda c: c in printable, dirty.value)


def clean_url(url):
    if url:
        if not url.lower().startswith('http'):
            url = 'http://' + url
        p = urlparse(url)
        url = "%s://%s%s" % (p.scheme, p.hostname.lower(), p.path)
        return url
    return None


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
