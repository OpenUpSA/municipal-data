from django.urls import re_path
from rest_framework import routers
from .. import views

router = routers.DefaultRouter()
router.register(r"financial_years", views.FinancialYearViewSet)
router.register(r"budget_phases", views.BudgetPhaseViewSet)
router.register(r"projects", views.ProjectViewSet)

urlpatterns = [
    re_path(r"^search", views.ProjectSearch.as_view(), name="search"),
    re_path(r"^coordinates", views.ProjectCoordinates.as_view(), name="coordinates"),
]
urlpatterns += router.urls
