from django.contrib.postgres.search import SearchQuery
from django.db.models import Count

# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from .. import models
from .. import serializers

import re
PHRASE_RE = re.compile(r'"([^"]*)("|$)')
from django.db.models import Q

class CoordinatesPagination(PageNumberPagination):
    page_query_param = "page"
    page_size = 500


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
        queryset = models.Project.objects.prefetch_related(
            "geography",
            "expenditure",
            "expenditure__budget_phase",
            "expenditure__financial_year",
        ).all()
        geo = self.request.query_params.get("geo", None)
        if geo is not None:
            queryset = queryset.filter(geography__geo_code=geo)
        return queryset

    def get_serializer_context(self, **kwargs):
        context = super(ProjectViewSet, self).get_serializer_context(**kwargs)
        if "full" in self.request.query_params:
            context["full"] = True
        return context


class ProjectCoordinates(generics.ListCreateAPIView):
    queryset = models.Project.objects.prefetch_related(
        "expenditure",
        "expenditure__budget_phase",
        "expenditure__financial_year",
        "geography",
    )
    serializer_class = serializers.GeoProjectSerializer
    pagination_class = CoordinatesPagination

    fieldmap = {
        "function": "function",
        "project_type": "project_type",
        "municipality": "geography__name",
        "province": "geography__province_name",
        "budget_phase": "expenditure__budget_phase__name",
        "financial_year": "expenditure__financial_year__budget_year",
    }

    def list(self, request):
        search_query = request.GET.get("q", "")
        queryset = self.get_queryset()
        queryset = self.filters(queryset, request.GET)
        queryset = self.text_search(queryset, search_query)
        queryset = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        return self.get_paginated_response(serializer.data)

    def text_search(self, qs, text):
        if len(text) == 0:
            return qs

        return qs.filter(content_search=SearchQuery(text))

    def filters(self, queryset, params):
        query_dict = {}
        for k, v in self.fieldmap.items():
            if k in params:
                query_dict[v] = params[k]

        return queryset.filter(**query_dict)


class ProjectSearch(generics.ListCreateAPIView):
    queryset = models.Project.objects.prefetch_related(
        "expenditure",
        "expenditure__budget_phase",
        "expenditure__financial_year",
        "geography",
    ).all()
    serializer_class = serializers.ProjectSerializer
    pagination_class = PageNumberPagination
    annual_fieldmap = {
        "geography__name": "municipality",
        "function": "function",
        "project_type": "project_type",
        "geography__province_name": "province",
        "expenditure__budget_phase__name": "budget_phase",
        "expenditure__financial_year__budget_year": "financial_year",
        "latest_implementation_year__budget_year": "financial_year",
    }

    quarterly_fieldmap = {
        "geography__name": "municipality",
        "function": "function",
        "project_type": "project_type",
        "geography__province_name": "province",
        "quarterly__financial_year__budget_year": "financial_year",
        "expenditure__budget_phase__name": "quarterly_phase",
    }

    order_fields = {
        "project_description": "project_description",
        "total_forecast_budget": "expenditure__amount",
        "project_type": "project_type",
        "function": "function",
    }

    def list(self, request):
        search_query = request.GET.get("q", "")
        order_field = request.GET.get("ordering", "")

        queryset = self.get_queryset()

        queryset = self.add_filters(queryset, request.GET, self.annual_fieldmap)
        queryset = self.text_search(queryset, search_query)

        queryset = queryset | self.add_filters(
            self.get_queryset(), request.GET, self.quarterly_fieldmap
        )
        queryset = self.text_search(queryset, search_query)

        facets = self.get_facets(queryset)
        queryset = self.order_by(queryset, order_field)
        aggregations = self.aggregations(queryset, request.GET)

        queryset = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        data = {
            "projects": serializer.data,
            "facets": facets,
            "aggregations": aggregations,
        }

        return self.get_paginated_response(data)

    def text_search(self, qs, text):
        if len(text) == 0:
            return qs

        search_field = "content_search"
        field_queries = Q()

        phrases = [p[0].strip() for p in PHRASE_RE.findall(text)]
        phrases = [p for p in phrases if p]
        terms = PHRASE_RE.sub("", text).strip()

        if terms:
            compound_statement = SearchQuery(terms, config="english")

        field_queries.add(Q(**{search_field: compound_statement}), Q.OR)

        print(field_queries)
        return qs.filter(field_queries)
        #return qs.filter(content_search=SearchQuery(text))

    def aggregations(self, qs, params):
        financial_year = params.get("financial_year")
        budget_phase = params.get("budget_phase")

        return {"total": qs.total_value(financial_year, budget_phase)}

    def add_filters(self, qs, params, filter_map):
        query_dict = {}
        for k, v in filter_map.items():
            if v in params:
                query_dict[k] = params[v]

        return qs.filter(**query_dict).distinct()

    def order_by(self, qs, field):
        prefix = ""
        if len(field) > 0 and field[0] == "-":
            prefix = "-"
            field = field[1:]

        order_by = ProjectSearch.order_fields.get(field, "-project_description")

        return qs.order_by(f"{prefix}{order_by}")

    def get_facets(self, qs):
        def facet_query(field):
            return qs.values(field).annotate(count=Count("id", distinct=True))

        facet_muni = facet_query("geography__name")
        facet_type = facet_query("project_type")
        facet_function = facet_query("function")
        facet_province = facet_query("geography__province_name")
        facet_json = {
            "municipality": facet_muni,
            "type": facet_type,
            "function": facet_function,
            "province": facet_province,
        }
        return facet_json
