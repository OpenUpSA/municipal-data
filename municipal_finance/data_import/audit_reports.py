# python municipal_finance/data_import/audit_reports.py |tee audit_reports.csv
# cat audit_reports.csv|grep -v "Thumbs.db"|cut -d, -f-2  | sort |uniq -c|sort -n|grep -v ' 1 '|cut -d' ' -f 8- > multi
# grep -f multi audit_reports.csv
#
# Multiple audit reports should only be for a municipality with entity(ies). In the case of some metros with many entities there should be an audit report for each entity, one for the parent municipality and one for the consolidated whole.  In the latter case - link to the consolidated audit report.

import requests
from bs4 import BeautifulSoup
import re
import sys

root = 'http://mfma.treasury.gov.za/'


def main():
    year_dirs = list(expand_dir('/Documents/07.%20Audit%20Reports/', {}))
    year_dirs.reverse()
    for year_dir in year_dirs:
        for category_dir in expand_dir(year_dir, {}):
            for muni_dir in expand_dir(category_dir, {}):
                report_paths = [p for p in list(expand_dir(muni_dir, {}))
                                if 'Thumbs.db' not in p]

                if len(report_paths) == 0:
                    pass
                elif len(report_paths) == 1:
                    to_csv(report_paths[0])
                elif len(report_paths) > 1:
                    to_csv(muni_dir)


# /Documents/07.%20Audit%20Reports/2003-04/02.%20Local%20municipalities/EC125%20Buffalo%20City/EC125%20Buffalo%20City%20Audit%20Report%202003-04.pdf
def to_csv(report_path):
    try:
        regex = '/Documents/07.%20Audit%20Reports/\d{4}-(\d{2})/[\w.%]+/(\w{3,6})'
        match = re.search(regex, report_path)
        print("%s,20%s,%s%s" % (match.group(2), match.group(1), root, report_path))
    except:
        print("\n  %s\n" % report_path)
    sys.stdout.flush()


def expand_dir(dir, params):
    params['SortField'] = 'LinkFilename'
    params['SortDir'] = 'Asc'
    # print("\nDir: %s %r" % (dir, params))
    r = requests.get(root + dir, params=params)
    r.raise_for_status()
    soup = BeautifulSoup(r.text.encode('utf8', 'replace'), "html.parser")
    for table in soup.find_all('table'):
        if u'url' in table.attrs:
            child_path = table.attrs[u'url']
            yield child_path
    next_arrow = soup.find(alt='Next')
    if next_arrow:
        # print
        # print("  Current dir=%s" % dir)
        # print("  Last child_path=%s" % child_path)
        last_name = child_path.replace(dir + '/', '')
        # print(last_name)
        # print
        for path in expand_dir(dir, {'p_FileLeafRef': last_name, 'Paged': 'TRUE'}):
            yield path


if __name__ == "__main__":
    main()
