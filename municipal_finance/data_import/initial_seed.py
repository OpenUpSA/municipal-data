import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'municipal_finance.settings'
sys.path.append("municipal_finance")

from utils import import_data
from resources import (
    AgedCreditorItemsV1Resource,
)


fixture_dir = 'municipal_finance/fixtures/initial/'

import_data(AgedCreditorItemsV1Resource, f'{fixture_dir}aged_creditor_items_v1.csv')
