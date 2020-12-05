from import_export import resources

from .models import (
    AmountType,
    AmountTypeV2,
    CflowItemsV1,
    CflowItemsV2,
    GovernmentFunctionsV1,
    GovernmentFunctionsV2,
    IncexpItemsV1,
    IncexpItemsV2,
    BsheetItemsV1,
    BsheetItemsV2,
    CapitalTypeV2,
    CapitalItemsV1,
    CapitalItemsV2,
    ConditionalGrantTypesV1,
    GrantTypesV2,
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


class BsheetItemsV1Resource(resources.ModelResource):
    class Meta:
        model = BsheetItemsV1
        import_id_fields = ['code']


class FinancialPositionItemsV2Resource(resources.ModelResource):
    class Meta:
        model = BsheetItemsV2
        import_id_fields = ['code']


class CapitalTypeV2Resource(resources.ModelResource):
    class Meta:
        model = CapitalTypeV2
        import_id_fields = ['code']


class CapitalItemsV1Resource(resources.ModelResource):
    class Meta:
        model = CapitalItemsV1
        import_id_fields = ['code']


class CapitalItemsV2Resource(resources.ModelResource):
    class Meta:
        model = CapitalItemsV2
        import_id_fields = ['code']


class ConditionalGrantTypesV1Resource(resources.ModelResource):
    class Meta:
        model = ConditionalGrantTypesV1
        import_id_fields = ['code']


class GrantTypesV2Resource(resources.ModelResource):
    class Meta:
        model = GrantTypesV2
        import_id_fields = ['code']
