from rest_framework import serializers

from . import models
from scorecard.serializers import GeographySerializer


class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FinancialYear
        fields = ["budget_year"]
        read_only_fields = ["budget_year"]


class BudgetPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BudgetPhase
        fields = ["code", "name"]
        read_only_fields = ["code", "name"]


class ExpenditureSerializer(serializers.ModelSerializer):
    financial_year = FinancialYearSerializer(read_only=True)
    budget_phase = BudgetPhaseSerializer(read_only=True)

    class Meta:
        model = models.Expenditure
        fields = ["amount", "budget_phase", "financial_year"]
        read_only_fields = ["amount", "budget_phase", "financial_year"]


class ProjectSerializer(serializers.ModelSerializer):
    expenditure = ExpenditureSerializer(many=True, read_only=True)
    geography = GeographySerializer(read_only=True)

    class Meta:
        model = models.Project
        fields = "__all__"
        read_only_fields = [
            "function",
            "project_description",
            "project_number",
            "project_type",
            "mtsf_service_outcome",
            "iudf",
            "own_strategic_objectives",
            "asset_class",
            "asset_subclass",
            "ward_location",
            "longitude",
            "latitude",
        ]


class GeoProjectSerializer(serializers.ModelSerializer):
    expenditure = ExpenditureSerializer(many=True, read_only=True)

    class Meta:
        model = models.Project
        fields = ("project_description", "latitude", "longitude", "expenditure")
        read_only_fields = ["project_description", "latitude", "longitude"]
