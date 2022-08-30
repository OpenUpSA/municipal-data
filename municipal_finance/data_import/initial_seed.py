from ..utils import import_data
from ..resources import (
    AgedCreditorItemsV1Resource,
)


fixture_dir = 'municipal_finance/fixtures/initial/'

import_data(AgedCreditorItemsV1Resource, f'{fixture_dir}aged_creditor_items_v1.csv')
