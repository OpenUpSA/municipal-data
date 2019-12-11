from rest_framework import viewsets

from .. import models
from .. import serializers

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

    def get_serializer_context(self, **kwargs):
        context = super(ProjectViewSet, self).get_serializer_context(**kwargs)
        if "full" in self.request.query_params:
            context["full"] = True
        return context


