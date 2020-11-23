from import_export import resources

from municipal_finance.models import (
    CflowFactsV1,
    CflowFactsV2,
    IncexpFactsV1,
    IncexpFactsV2,
    BsheetFactsV1,
    BsheetFactsV2,
    CapitalFactsV1,
    CapitalFactsV2,
    UifwexpFacts,
)

from ...models import Geography


class GeographyResource(resources.ModelResource):
    class Meta:
        model = Geography
        import_id_fields = ['geo_code']


class IncexpFactsV1Resource(resources.ModelResource):
    class Meta:
        model = IncexpFactsV1
        import_id_fields = [
            'demarcation_code',
            'period_code',
            'item_code',
            'function_code',
        ]


class IncexpFactsV2Resource(resources.ModelResource):
    class Meta:
        model = IncexpFactsV2
        import_id_fields = [
            'demarcation_code',
            'period_code',
            'item',
            'function',
        ]


class BsheetFactsV1Resource(resources.ModelResource):
    class Meta:
        model = BsheetFactsV1
        import_id_fields = [
            'demarcation_code',
            'period_code',
            'item_code',
        ]


class BsheetFactsV2Resource(resources.ModelResource):
    class Meta:
        model = BsheetFactsV2
        import_id_fields = [
            'demarcation_code',
            'period_code',
            'item',
        ]


class CapitalFactsV1Resource(resources.ModelResource):
    class Meta:
        model = CapitalFactsV1
        import_id_fields = [
            'demarcation_code',
            'period_code',
            'item_code',
            'function_code',
        ]


class CapitalFactsV2Resource(resources.ModelResource):
    class Meta:
        model = CapitalFactsV2
        import_id_fields = [
            'demarcation_code',
            'period_code',
            'item',
            'function',
            'capital_type',
        ]


class UIFWExpenditureFactsResource(resources.ModelResource):
    class Meta:
        model = UifwexpFacts
        import_id_fields = [
            'demarcation_code',
            'financial_year',
            'item_code',
        ]


class CashflowFactsV1Resource(resources.ModelResource):
    class Meta:
        model = CflowFactsV1
        import_id_fields = [
            'demarcation_code',
            'period_code',
            'item_code',
        ]


class CashflowFactsV2Resource(resources.ModelResource):
    class Meta:
        model = CflowFactsV2
        import_id_fields = [
            'demarcation_code',
            'period_code',
            'item',
        ]
