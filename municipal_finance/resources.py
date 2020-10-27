from import_export import resources

from .models import CflowItemsMSCOA


class CashflowItemsMSCOAResource(resources.ModelResource):
    class Meta:
        model = CflowItemsMSCOA
        import_id_fields = ['code']
