from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic.base import TemplateView

from . import models
from . import serializers

class FinancialYearViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.FinancialYear.objects.all()
    serializer_class = serializers.FinancialYearSerializer

class BudgetPhaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.BudgetPhase.objects.all()
    serializer_class = serializers.BudgetPhaseSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        queryset = models.Project.objects.all()
        geo = self.request.query_params.get('geo', None)
        if geo is not None:
            queryset = queryset.filter(geography__geo_code=geo)
        return queryset

class ListView(TemplateView):

    template_name = 'infrastructure/list.html'
