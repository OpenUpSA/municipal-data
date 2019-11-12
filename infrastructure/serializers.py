from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer
from drf_haystack.serializers import HaystackFacetSerializer
from drf_haystack.serializers import HaystackSerializerMixin

from . import models
from . import search_indexes
from scorecard.serializers import GeographySerializer


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
    geography = GeographySerializer(read_only=True)

    class Meta:
        model = models.Project
        fields = "__all__"

class ProjectSearchSerializer(HaystackSerializerMixin, ProjectSerializer):

    class Meta(ProjectSerializer.Meta):
        index_classes = [search_indexes.ProjectIndex]

        search_fields = ("text",) 


class ProjectFacetSerializer(HaystackFacetSerializer):

    class Meta:
        index_classes = [search_indexes.ProjectIndex]
        fields = ["function", "project_type", "asset_class", "asset_subclass", "province"]
        field_options = {
            "function" : {},
            "project_type" : {},
            "asset_class" : {},
            "asset_subclass" : {},
            "province" : {},
            "geography_name" : {},
            "geo_code" : {},
            "geo_parent" : {},
        }
