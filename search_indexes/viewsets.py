from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
)

from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    CompoundSearchFilterBackend,
    FacetedSearchFilterBackend,
    aggregations,
)

from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from elasticsearch_dsl import TermsFacet
from elasticsearch_dsl.faceted_search import Facet

from .documents import ProjectDocument
from .serializers import ProjectDocumentSerializer

from .backends import AggregationsBackend

class MunicipalBudgetFacet(TermsFacet):
    def get_aggregation(self):
        agg = super(MunicipalBudgetFacet, self).get_aggregation()

    
        """
        Return the aggregation object.
        """
        agg = A(self.agg_type, **self._params)
        if self._metric:
            agg.metric('metric', self._metric)
        return agg

class SumFacet(Facet):
    agg_type = 'sum'

from rest_framework.decorators import action
class ProjectDocumentView(DocumentViewSet):

    document = ProjectDocument
    serializer_class = ProjectDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = "id"

    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        FacetedSearchFilterBackend,
        AggregationsBackend,
    ]

    # Define search fields
    search_fields = (
        #"id",
        "project_description",
        "project_number",
        "function",
        "project_type",
        "province",
        "municipality",
        "mtsf_service_outcome",
        "iudf",
        "own_strategic_objectives",
        "asset_class",
        "asset_subclass",
    )

    # Define filter fields
    filter_fields = {
        "id": {
            "field": "id",
            # Note, that we limit the lookups of id field in this example,
            # to `range`, `in`, `gt`, `gte`, `lt` and `lte` filters.
            "lookups": [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        "function": "function",
        "project_type": "project_type",
        "province": "province",
        "municipality": "municipality",
        "pages": {
            "field": "pages",
            # Note, that we limit the lookups of `pages` field in this
            # example, to `range`, `gt`, `gte`, `lt` and `lte` filters.
            "lookups": [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
    }

    faceted_search_fields = {
         #"id": {
         #    "field": "id",
         #},
         "province": {
             "field": "province",
             #"facet": TermsFacet,
             "enabled": True,
         },
         "municipality": {
             "field": "municipality",
             "facet": TermsFacet,
             "enabled": True,
             "options": {
                "size" : 300
            }
         },
         "functions": {
             "field": "function",
             "facet": TermsFacet,
             "enabled": True,
             "options": {
                "size" : 300
            }
         },
         "project_type": {
             "field": "project_type",
             "facet": TermsFacet,
             "enabled": True
         },
         "total_budget": {
            "field": "total_forecast_budget",
            "facet": SumFacet,
            "enabled": True
        },
    }

    ## Define ordering fields
    ordering_fields = {
    #    "id": "id",
        "total_forecast_budget": "total_forecast_budget",
        "province": "province",
        "project_description": "project_description",
        "function": "function",
        "project_type": "project_type",
    }
    ## Specify default ordering
    ordering = ("-total_forecast_budget",)
