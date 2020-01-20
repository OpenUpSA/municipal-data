from django.contrib.postgres.search import SearchQuery
from django.db.models import Count, Sum
from django.db.models import F

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
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

class ProjectSearch(generics.ListCreateAPIView):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    pagination_class = PageNumberPagination
    fieldmap = {
        "municipality": "geography__name",
        "function": "function",
        "type": "project_type",
        "province": "geography__province_name"
    }

    order_fields = {
        "project_description": "project_description",
        "total_forecast_budget": "project_description", # TODO still needs to be implemented
        "type": "project_type",
        "function": "function",
    }


    def list(self, request):
        search_query = request.GET.get("q", "")
        order_field = request.GET.get("ordering", "")

        queryset = self.get_queryset()
        queryset = self.add_filters(queryset, request.GET)
        queryset = self.text_search(queryset, search_query)
        queryset = self.order_by(queryset, order_field)
        facets = self.get_facets(queryset)
        aggregations = self.aggregations(queryset, request.GET)

        queryset = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        data = {
            "projects": serializer.data,
            "facets": facets,
            "aggregations": aggregations
        } 

        return self.get_paginated_response(data)

    def text_search(self, qs, text):
        if len(text) == 0:
            return qs
        
        return qs.filter(content_search=SearchQuery(text))

    def aggregations(self, qs, params):
        # TODO - not sure where to put these magic values
        financial_year = params.get("financial_year", "2017/2018")
        budget_phase = params.get("budget_phase", "Audited Outcome")

        return {
            "total": qs.total_value(financial_year, budget_phase)

        }

    def add_filters(self, qs, params):
        query_dict = {}
        for k, v in ProjectSearch.fieldmap.items():
            if k in params:
                query_dict[v] = params[k]

        return qs.filter(**query_dict)

    def order_by(self, qs, field):
        prefix = ""
        if len(field) > 0 and field[0] == "-":
            prefix = "-"
            field = field[1:]

        order_by = ProjectSearch.order_fields.get(field, "-project_description")

        return qs.order_by(f"{prefix}{order_by}")


    def get_facets(self, qs):
        def facet_query(field):
            field_name = F(field)
            return qs.values(key=F(field)).annotate(count=Count(field))


        facet_muni = facet_query("geography__name")
        facet_type = facet_query("project_type")
        facet_function = facet_query("function")
        facet_province = facet_query("geography__province_name")
        js = {
            "municipality": facet_muni,
            "type": facet_type,
            "function": facet_function,
            "province": facet_province
        }
        return js


