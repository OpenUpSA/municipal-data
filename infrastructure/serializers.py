from infrastructure import models
from rest_framework import serializers


class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FinancialYear
        fields = ["budget_year"]


class BudgetPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BudgetPhase
        fields = ["code", "name"]


class ExpenditureSerializer(serializers.ModelSerializer):
    financial_year = FinancialYearSerializer(read_only=True)
    budget_phase = BudgetPhaseSerializer(read_only=True)

    class Meta:
        model = models.Expenditure
        fields = ["amount", "budget_phase", "financial_year"]

class ProjectSerializer(serializers.ModelSerializer):
    expenditure = ExpenditureSerializer(many=True, read_only=True)

    class Meta:
        model = models.Project
        fields = "__all__"

