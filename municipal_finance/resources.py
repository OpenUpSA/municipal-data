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
    FinancialPositionItemsV2,
    CapitalTypeV2,
    CapitalItemsV1,
    CapitalItemsV2,
    ConditionalGrantTypesV1,
    GrantTypesV2,
    RepairsMaintenanceItemsV1,
    RepairsMaintenanceItemsV2,
    AgedDebtorItemsV1,
    AgedDebtorItemsV2,
    AgedCreditorItemsV1,
    AgedCreditorItemsV2,
)


class AmountTypeV1Resource(resources.ModelResource):
    class Meta:
        model = AmountType
        import_id_fields = ("code",)


class AmountTypeV2Resource(resources.ModelResource):
    class Meta:
        model = AmountTypeV2
        import_id_fields = ("code",)
        fields = ("code", "label",)


class CashflowItemsV1Resource(resources.ModelResource):
    class Meta:
        model = CflowItemsV1
        import_id_fields = ("code",)


class CashflowItemsV2Resource(resources.ModelResource):
    class Meta:
        model = CflowItemsV2
        import_id_fields = ("code",)
        fields = (
            "code",
            "label",
            "position_in_return_form",
            "return_form_structure",
            "composition",
        )


class GovernmentFunctionsV1Resource(resources.ModelResource):
    class Meta:
        model = GovernmentFunctionsV1
        import_id_fields = ("code",)


class GovernmentFunctionsV2Resource(resources.ModelResource):
    class Meta:
        model = GovernmentFunctionsV2
        import_id_fields = ("code",)
        fields = (
            "code",
            "label",
            "category_label",
            "subcategory_label",
        )


class IncexpItemsV1Resource(resources.ModelResource):
    class Meta:
        model = IncexpItemsV1
        import_id_fields = ("code",)


class IncexpItemsV2Resource(resources.ModelResource):
    class Meta:
        model = IncexpItemsV2
        import_id_fields = ("code",)
        fields = (
            "code",
            "label",
            "position_in_return_form",
            "return_form_structure",
            "composition",
        )


class BsheetItemsV1Resource(resources.ModelResource):
    class Meta:
        model = BsheetItemsV1
        import_id_fields = ("code",)


class FinancialPositionItemsV2Resource(resources.ModelResource):
    class Meta:
        model = FinancialPositionItemsV2
        import_id_fields = ("code",)
        fields = (
            "code",
            "label",
            "position_in_return_form",
            "return_form_structure",
            "composition",
        )


class CapitalTypeV2Resource(resources.ModelResource):
    class Meta:
        model = CapitalTypeV2
        import_id_fields = ("code",)
        fields = ("code", "label",)


class CapitalItemsV1Resource(resources.ModelResource):
    class Meta:
        model = CapitalItemsV1
        import_id_fields = ("code",)


class CapitalItemsV2Resource(resources.ModelResource):
    class Meta:
        model = CapitalItemsV2
        import_id_fields = ("code",)
        fields = (
            "code",
            "label",
            "position_in_return_form",
            "return_form_structure",
            "composition",
        )


class ConditionalGrantTypesV1Resource(resources.ModelResource):
    class Meta:
        model = ConditionalGrantTypesV1
        import_id_fields = ("code",)


class GrantTypesV2Resource(resources.ModelResource):
    class Meta:
        model = GrantTypesV2
        import_id_fields = ("code",)
        fields = ("code", "name",)


class RepairsMaintenanceItemsV1Resource(resources.ModelResource):
    class Meta:
        model = RepairsMaintenanceItemsV1
        import_id_fields = ("code",)


class RepairsMaintenanceItemsV2Resource(resources.ModelResource):
    class Meta:
        model = RepairsMaintenanceItemsV2
        import_id_fields = ("code",)
        fields = (
            "code",
            "label",
            "position_in_return_form",
            "return_form_structure",
            "composition",
        )


class AgedDebtorItemsV1Resource(resources.ModelResource):
    class Meta:
        model = AgedDebtorItemsV1
        import_id_fields = ("code",)


class AgedDebtorItemsV2Resource(resources.ModelResource):
    class Meta:
        model = AgedDebtorItemsV2
        import_id_fields = ("code",)
        fields = (
            "code",
            "label",
            "position_in_return_form",
            "return_form_structure",
            "composition",
        )


class AgedCreditorItemsV1Resource(resources.ModelResource):
    class Meta:
        model = AgedCreditorItemsV1
        import_id_fields = ("code","id")


class AgedCreditorItemsV2Resource(resources.ModelResource):
    class Meta:
        model = AgedCreditorItemsV2
        import_id_fields = ("code",)
        fields = (
            "code",
            "label",
            "position_in_return_form",
            "return_form_structure",
            "composition",
        )
