"""
python contact_details.py 'Municipal contact detail - 28 April 2016.xlsx' 'muni.csv' 'persons.csv'
python -m pdb muni_contacts.py 'Municipal contact detail - 28 April 2016.xlsx' 'muni.csv' 'persons.csv'
"""
import csv
import string
import sys
import xlrd
from urllib.parse import urlparse

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
    'Position',
    'ID Number',
    'Title',
    'Name',
    'Office Phone Number',
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
    check_columns(get_headings(sheet))
    convert_persons(sheet, person_csv_name)
    convert_muni(sheet, muni_csv_name)


def col(heading):
    return expected_headings.index(heading)


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
        for rowx in range(1, sheet.nrows):
            if str(sheet.cell(rowx, col("CAP")).value) not in ['H', 'L', 'M']:
                continue
            role = sheet.cell(rowx, col("Position")).value
            check_role(role)
            if role not in output_roles:
                continue
            item = {
                'demarcation_code': sheet.cell(rowx, col("Locat Code")).value,
                'role': role,
                'title': sheet.cell(rowx, col("Title")).value,
                'name': clean(sheet.cell(rowx, col("Name"))),
                'office_number': sheet.cell(rowx, col("Office Phone Number")).value,
                # Hack because Fax Number occurs twice
                'fax_number': sheet.cell(rowx, col("Cell Number")+1).value,
                'email_address': sheet.cell(rowx, col("EMAILADD")).value,
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
        for rowx in range(1, sheet.nrows):
            if str(sheet.cell(rowx, col("CAP")).value) not in ['H', 'L', 'M']:
                continue

            # Do each muni only once
            if sheet.cell(rowx, col("Locat Code")).value == muni:
                continue
            else:
                muni = sheet.cell(rowx, col("Locat Code")).value

            item = {
                'demarcation_code': muni,
                'postal_address_1': clean(sheet.cell(rowx, col("Postal Address 1"))),
                'postal_address_2': clean_address(sheet.cell(rowx, col("Postal Address 2"))),
                'postal_address_3': clean_address(sheet.cell(rowx, col("Postal Address 3"))),
                'street_address_1': clean(sheet.cell(rowx, col("Street Address 1"))),
                'street_address_2': clean_address(sheet.cell(rowx, col("Street Address 2"))),
                'street_address_3': clean_address(sheet.cell(rowx, col("Street Address 3"))),
                'street_address_4': clean_address(sheet.cell(rowx, col("Street Address 4"))),
                'phone_number': clean(sheet.cell(rowx, col("Phone Number"))),
                'fax_number': clean(sheet.cell(rowx, col("Fax Number"))),
                'url': clean_url(sheet.cell(rowx, col("E-mail Address")).value),
            }
            writer.writerow(item)


def normalize(name):
    return name.replace(' ', '').replace('\n', '')


def get_headings(sheet):
    headings = []
    for colx in range(0, sheet.ncols):
        headings.append(
            normalize(str(sheet.cell(1, colx).value))
        )
    return headings


def check_columns(headings):
    for colx in range(0, len(headings)):
        heading = headings[colx]
        expected_heading = normalize(expected_headings[colx])
        if heading != expected_heading:
            raise Exception("Unexpected heading %r != %r <- expected"
                            % (heading, expected_headings[colx]))


def clean(dirty):
    if dirty.ctype == 2:
        return str(int(dirty.value))
    else:
        return ''.join(filter(lambda c: c in printable, dirty.value))


def clean_address(dirty):
    """zero-pad if it looks like 4-digit post codes"""
    if dirty.ctype == 2:
        return format(int(dirty.value), '04')
    else:
        return ''.join(filter(lambda c: c in printable, dirty.value))


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
    convert(workbook_name, muni_csv_name, person_csv_name)


if __name__ == "__main__":
    main()
