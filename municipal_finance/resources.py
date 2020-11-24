from import_export import resources

from .models import (
    AmountType,
    AmountTypeV2,
    CflowItemsV1,
    CflowItemsV2,
    CflowFactsV1,
    CflowFactsV2,
    GovernmentFunctionsV1,
    GovernmentFunctionsV2,
    IncexpItemsV1,
    IncexpItemsV2,
    IncexpFactsV1,
    IncexpFactsV2,
    BsheetItemsV1,
    BsheetItemsV2,
    BsheetFactsV1,
    BsheetFactsV2,
)


class AmountTypeV1Resource(resources.ModelResource):
    class Meta:
        model = AmountType
        import_id_fields = ['code']


class AmountTypeV2Resource(resources.ModelResource):
    class Meta:
        model = AmountTypeV2
        import_id_fields = ['code']


class CashflowItemsV1Resource(resources.ModelResource):
    class Meta:
        model = CflowItemsV1
        import_id_fields = ['code']


class CashflowItemsV2Resource(resources.ModelResource):
    class Meta:
        model = CflowItemsV2
        import_id_fields = ['code']


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


class GovernmentFunctionsV1Resource(resources.ModelResource):
    class Meta:
        model = GovernmentFunctionsV1
        import_id_fields = ['code']


class GovernmentFunctionsV2Resource(resources.ModelResource):
    class Meta:
        model = GovernmentFunctionsV2
        import_id_fields = ['code']


class IncexpItemsV1Resource(resources.ModelResource):
    class Meta:
        model = IncexpItemsV1
        import_id_fields = ['code']


class IncexpItemsV2Resource(resources.ModelResource):
    class Meta:
        model = IncexpItemsV2
        import_id_fields = ['code']


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


class BsheetItemsV1Resource(resources.ModelResource):
    class Meta:
        model = BsheetItemsV1
        import_id_fields = ['code']


class FinancialPositionItemsV2Resource(resources.ModelResource):
    class Meta:
        model = BsheetItemsV2
        import_id_fields = ['code']


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
