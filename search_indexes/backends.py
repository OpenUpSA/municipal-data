from elasticsearch_dsl import A
from rest_framework.filters import BaseFilterBackend

class AggregationsBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        s = queryset

        a = A("sum", field="total_forecast_budget")
        s.aggs.metric("myval", "sum", field="total_forecast_budget")
        return queryset

