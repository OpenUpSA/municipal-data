from django.contrib import admin

from .models import FinancialYear, BudgetPhase, HouseholdClass, HouseholdService, HouseholdBill,HouseholdIncrease


admin.site.register(FinancialYear)
admin.site.register(BudgetPhase)
admin.site.register(HouseholdClass)
admin.site.register(HouseholdService)
admin.site.register(HouseholdBill)
admin.site.register(HouseholdIncrease)
