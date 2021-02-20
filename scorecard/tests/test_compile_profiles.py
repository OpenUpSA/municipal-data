
from itertools import groupby

from . import _ApiTestCase, import_data

from .resources import (
    GeographyResource,
    DemarcationChangesResource,
)

from ..compile_profiles import get_municipalities


class CompileProfilesTestCase(_ApiTestCase):

    def test_get_municipalities(self):
        import_data(
            GeographyResource,
            "compile_profiles/scorecard_geography.csv",
        )
        import_data(
            DemarcationChangesResource,
            "compile_profiles/municipal_finance_demarcationchanges.csv",
        )
        result = get_municipalities(self.api_client)
        self.assertEquals(result, [
            {
                "geo_code": "EC101",
                "miif_category": "B3",
                "province_code": "EC",
                "disestablished": False,
            },
            {
                "geo_code": "EC103",
                "miif_category": "B3",
                "province_code": "EC",
                "disestablished": True,
                "disestablished_date": "2016-08-03",
            },
            {
                "geo_code": "EC137",
                "miif_category": "B4",
                "province_code": "EC",
                "disestablished": False,
            },
        ])

