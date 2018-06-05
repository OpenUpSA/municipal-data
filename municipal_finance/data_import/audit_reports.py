# python municipal_finance/data_import/audit_reports.py audit_reports.csv
# cat audit_reports.csv|grep -v "Thumbs.db"|cut -d, -f-2  | sort |uniq -c|sort -n|grep -v ' 1 '|cut -d' ' -f 8- > multi
# grep -f multi audit_reports.csv
#
# Multiple audit reports should only be for a municipality with entity(ies). In the case of some metros with many entities there should be an audit report for each entity, one for the parent municipality and one for the consolidated whole.  In the latter case - link to the consolidated audit report.

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import csv
import re
import requests
import sys
import traceback
import logging

root = 'http://mfma.treasury.gov.za'
fieldnames = ['demarcation_code', 'year', 'url']


class Main(object):
    def __init__(self, csv_file):
            self.writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            self.writer.writeheader()
            self.session = requests.Session()
            self.session.mount(root, HTTPAdapter(max_retries=5))

    def run(self):
        year_dirs = list(self.expand_dir('/Documents/07.%20Audit%20Reports/', {}))
        year_dirs.reverse()
        for year_dir in year_dirs:
            for category_dir in self.expand_dir(year_dir, {}):
                for muni_dir in self.expand_dir(category_dir, {}):
                    report_paths = [p for p in list(self.expand_dir(muni_dir, {}))
                                    if 'Thumbs.db' not in p]

                    if len(report_paths) == 0:
                        pass
                    elif len(report_paths) == 1:
                        self.writerow(report_paths[0])
                    elif len(report_paths) > 1:
                        self.writerow(muni_dir)


    # /Documents/07.%20Audit%20Reports/2003-04/02.%20Local%20municipalities/EC125%20Buffalo%20City/EC125%20Buffalo%20City%20Audit%20Report%202003-04.pdf
    def writerow(self, report_path):
        try:
            regex = '/Documents/07.%20Audit%20Reports/\d{4}-(\d{2})/[\w.%]+/(\w{3,6})'
            match = re.search(regex, report_path)
            self.writer.writerow({
                'demarcation_code': match.group(2),
                'year': '20' + match.group(1),
                'url': root + report_path,
            })
        except:
            print("\nerror  %s\n" % report_path)
            traceback.print_exc()
            sys.stdout.flush()

    def expand_dir(self, dir, params):
        params['SortField'] = 'LinkFilename'
        params['SortDir'] = 'Asc'
        print("\nDir: %s %r" % (dir, params))
        try:
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
                print("  Current dir=%s" % dir)
                print("  Last child_path=%s" % child_path)
                last_name = child_path.replace(dir + '/', '')
                # print(last_name)
                # print
                for path in self.expand_dir(dir, {'p_FileLeafRef': last_name, 'Paged': 'TRUE'}):
                    yield path
        except:
            print("error", dir, params)
            traceback.print_exc()
            sys.stdout.flush()

if __name__ == "__main__":
    [outfile] = sys.argv[1:]
    with open(outfile, 'w') as csv_file:
        Main(csv_file).run()
