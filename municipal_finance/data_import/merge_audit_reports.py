import pdb
import sys
import traceback
import pandas as pd

def merge(opinions, reports):
    opinion_data = pd.read_csv(opinions)
    report_data = pd.read_csv(reports)
    report_data = report_data.drop('year', 1)

    output = pd.merge(opinion_data, report_data, on='demarcation_code', how='left')
    output.to_csv('file_name', index=False, sep=',')

def main():
    [opinions, reports] = sys.argv[1:]
    try:
        merge(opinions, reports)
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)

if __name__ == "__main__":
    main()
