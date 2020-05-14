from django.test import TestCase
from scorecard.models import Geography

from metro import models


class MetroTestCase(TestCase):
    def setUp(self):
        geography_jhb = Geography.objects.create(
                    geo_level="municipality",
                    geo_code="JHB",
                    name="City of Johannesburg",
                    parent_level="province",
                    parent_code="GT",
                    category="A",
                )
        geography_cpt = Geography.objects.create(
                    geo_level="municipality",
                    geo_code="CPT",
                    name="City of Cape Town",
                    parent_level="province",
                    parent_code="WC",
                    category="A",
                )
        
        category = models.Category.objects.create(
            name="Energy and Electricity", code="EE", slug="energy-and-electricity"
        )
        year = models.FinancialYear.objects.create(budget_year="2019/202", active=True)
        indicator_number = models.Indicator.objects.create(
            category=category
            name="Number of dwellings provided with connections to mains electricity supply by the municipality",
            code="EE1.11",
            tier="Tier 1",
            measurement="Number of Connections",
            reporting="National",
            alignment="Improved access to electricity",
            frequency="Quarterly",
            target="1500",
        )
        indicator_percent=models.Indicator.objects.create(
            category=category
            name="Percentage of households with access to electricity",
            code="EE2.11",
            tier="Tier 1",
            measurement="Number of Connections",
            reporting="National",
            alignment="Improved access to electricity",
            frequency="Quarterly",
            target="80%",
        )
        models.IndicatorQuarterResult.objects.create(
            indicator=indicator_number,
            geography=geography_jhb,
            financial_year=year,
            quarter_one = "150",
            quarter_two='1000',
            quarter_three='200'
        )
         models.IndicatorQuarterResult.objects.create(
            indicator=indicator_percent,
            geography=geography_jhb,
            financial_year=year,
            quarter_one = "20%",
            quarter_two='30%',
            quarter_three='10%'
        )
        models.IndicatorQuarterResult.objects.create(
            indicator=indicator_number,
            geography=geography_cpt,
            financial_year=year,
            quarter_one = "1000",
            quarter_two='500',
            quarter_three='20'
        )
         models.IndicatorQuarterResult.objects.create(
            indicator=indicator_percent,
            geography=geography_cpt,
            financial_year=year,
            quarter_one = "10%",
            quarter_two='50%',
            quarter_three='40%'
        )

    def test_number_target_achived(self):
        result_jhb = IndicatorQuarterResult.objects.get(quarter_one='150')
        result_cpt = IndicatorQuarterResult.objects.get(quarter_one='1000')
        self.assertEqual(result_jhb.target_achived, False)
        self.assertEqual(result_cpt.target_achived, True)
        

    def percent_target_achived_test(self):
        result_jhb = IndicatorQuarterResult.objects.get(quarter_one='20%')
        result_cpt = IndicatorQuarterResult.objects.get(quarter_one='10%')
        self.assertEqual(result_jhb.target_achived, False)
        self.assertEqual(result_cpt.target_achived, True)
    def category_sort_test(self):
        pass
