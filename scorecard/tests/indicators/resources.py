from import_export import resources

from municipal_finance.tests.resources import (
    IncexpFactsV1Resource,
    IncexpFactsV2Resource,
    CashFlowFactsV1Resource,
    CashFlowFactsV2Resource,
    BsheetFactsV1Resource,
    FinancialPositionFactsV2Resource,
    CapitalFactsV1Resource,
    CapitalFactsV2Resource,
    UIFWExpenditureFactsResource,
)

from ...models import Geography


class GeographyResource(resources.ModelResource):
    class Meta:
        model = Geography
        import_id_fields = ['geo_code']
