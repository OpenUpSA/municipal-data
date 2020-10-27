from import_export import resources

from .models import AmountType, CflowItemsMSCOA


class AmountTypeResource(resources.ModelResource):
    class Meta:
        model = AmountType
        import_id_fields = ['code']


class CashflowItemsMSCOAResource(resources.ModelResource):
    class Meta:
        model = CflowItemsMSCOA
        import_id_fields = ['code']
