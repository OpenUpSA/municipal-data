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
import urllib.parse
import time

root = "http://mfma.treasury.gov.za"
fieldnames = ["demarcation_code", "year", "url"]


class Main(object):
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        self.writer.writeheader()
        self.session = requests.Session()
        self.session.mount(root, HTTPAdapter(max_retries=5))

    def run(self):
        year_dirs = list(self.expand_dir("/Documents/07.%20Audit%20Reports/", {}))
        year_dirs.reverse()
        for year_dir in year_dirs:
            for category_dir in self.expand_dir(year_dir, {}):
                for muni_dir in self.expand_dir(category_dir, {}):
                    report_paths = [
                        p
                        for p in list(self.expand_dir(muni_dir, {}))
                        if "Thumbs.db" not in p
                    ]

                    if len(report_paths) == 0:
                        pass
                    elif len(report_paths) == 1:
                        self.writerow(report_paths[0])
                    elif len(report_paths) > 1:
                        querystring = urllib.parse.urlsplit(muni_dir).query
                        directory = urllib.parse.parse_qs(querystring)["RootFolder"][0]
                        self.writerow(directory)

    # /Documents/07. Audit Reports/2003-04/02. Local municipalities/EC125 Buffalo City/EC125 Buffalo City Audit Report 2003-04.pdf
    def writerow(self, report_path):
        try:
            regex = "/Documents/07\. Audit Reports/\d{4}-(\d{2})/[^/]+/(\w{3,6})"
            match = re.search(regex, report_path)
            self.writer.writerow(
                {
                    "demarcation_code": match.group(2),
                    "year": "20" + match.group(1),
                    "url": root + urllib.parse.quote(report_path),
                }
            )
            self.csv_file.flush()
        except:
            print("\nerror  %s\n" % report_path)
            traceback.print_exc()
            sys.stdout.flush()

    def expand_dir(self, dir, params):
        params["p_SortBehavior"] = "1"
        print("\nDir: %s %r" % (dir, params))
        try:
            r = requests.get(root + dir, params=params)

            while r.status_code == 429:
                time.sleep(11)
                r = requests.get(root + dir, params=params)
            r.raise_for_status()
            soup = BeautifulSoup(r.text.encode("utf8", "replace"), "html.parser")
            for anchor in soup.select('table[Field="LinkFilename"] a'):
                child_path = anchor.attrs["href"]
                yield child_path
            next_arrow = soup.find(alt="Next")
            if next_arrow:
                # print
                print("  Current dir=%s" % dir)
                print("  Last child_path=%s" % child_path)
                child_path_no_qs = urllib.parse.parse_qs(
                    urllib.parse.urlsplit(child_path).query
                )["RootFolder"][0]
                regex = ".+\/(.+)$"
                last_name = re.search(regex, child_path_no_qs).group(1)
                print("    last_name=%s" % last_name)
                # print
                for path in self.expand_dir(
                    dir, {"p_FileLeafRef": last_name, "Paged": "TRUE"}
                ):
                    print("    NEXT %s" % path)
                    yield path
        except:
            print("error", dir, params)
            traceback.print_exc()
            sys.stdout.flush()


if __name__ == "__main__":
    [outfile] = sys.argv[1:]
    with open(outfile, "w") as csv_file:
        Main(csv_file).run()
