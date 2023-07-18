from django.test import TransactionTestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django_q.models import OrmQ

from ...admin import IncomeExpenditureV2UpdateAdmin
from ...models import IncomeExpenditureV2Update


class IncomeExpenditureV2UpdateTestCase(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username='super',
            email='super@email.org',
            password='pass',
        )
        self.model_admin = IncomeExpenditureV2UpdateAdmin(
            model=IncomeExpenditureV2Update,
            admin_site=AdminSite(),
        )

    def test_save_task_trigger(self):
        request = self.factory.get(
            '/admin/municipal_finance/incomeexpenditurev2update/add/'
        )
        request.user = self.user
        obj = IncomeExpenditureV2Update()
        self.model_admin.save_model(
            obj=obj,
            request=request,
            form=None,
            change=None,
        )
        self.assertEquals(obj.user, self.user)
        record = OrmQ.objects.get(id=2)
        self.assertEquals(
            record.func(),
            'municipal_finance.update.update_income_expenditure_v2',
        )
