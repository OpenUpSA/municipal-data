from infrastructure import models
from rest_framework import serializers


class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FinancialYear
        fields = "__all__"


class BudgetPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BudgetPhase
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = "__all__"


class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expenditure
        fields = "__all__"
