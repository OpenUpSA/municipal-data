from django.shortcuts import render
from rest_framework.views import APIView


from . import models
from . import serializers
from rest_framework import viewsets

class FinancialYearViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.FinancialYear.objects.all()
    serializer_class = serializers.FinancialYearSerializer

class BudgetPhaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.BudgetPhase.objects.all()
    serializer_class = serializers.BudgetPhaseSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
