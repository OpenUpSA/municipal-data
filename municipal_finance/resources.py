from import_export import resources

from .models import (
    AmountTypeV2,
    CflowItemsV2,
    GovernmentFunctionsV2,
    IncexpItemsV2,
    BsheetItemsV1,
    BsheetItemsV2,
    BsheetFactsV1,
    BsheetFactsV2,
)


class AmountTypeV2Resource(resources.ModelResource):
    class Meta:
        model = AmountTypeV2
        import_id_fields = ['code']


class CashflowItemsV2Resource(resources.ModelResource):
    class Meta:
        model = CflowItemsV2
        import_id_fields = ['code']


class GovernmentFunctionsV2Resource(resources.ModelResource):
    class Meta:
        model = GovernmentFunctionsV2
        import_id_fields = ['code']


class IncexpItemsV2Resource(resources.ModelResource):
    class Meta:
        model = IncexpItemsV2
        import_id_fields = ['code']


class BsheetItemsV1Resource(resources.ModelResource):
    class Meta:
        model = BsheetItemsV1
        import_id_fields = ['code']


class FinancialPositionItemsV2Resource(resources.ModelResource):
    class Meta:
        model = BsheetItemsV2
        import_id_fields = ['code']


class BsheetFactsV2Resource(resources.ModelResource):
    class Meta:
        model = BsheetFactsV2
        import_id_fields = [
            'demarcation_code',
            'period_code',
            'item',
        ]


class BsheetFactsV1Resource(resources.ModelResource):
    class Meta:
        model = BsheetFactsV1
        import_id_fields = [
            'demarcation_code',
            'period_code',
            'item_code',
        ]
