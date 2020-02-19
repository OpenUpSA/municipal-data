from django.conf.urls import include, url
from rest_framework import routers
from .. import views

router = routers.DefaultRouter()
router.register(r"financial_years", views.FinancialYearViewSet)
router.register(r"budget_phases", views.BudgetPhaseViewSet)
router.register(r"projects", views.ProjectViewSet)

urlpatterns = [
    url(r"^search", views.ProjectSearch.as_view(), name="search"),
    url(r"^coordinates", views.ProjectCoordinates.as_view(), name="coordinates"),
]
urlpatterns += router.urls
