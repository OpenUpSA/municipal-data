import json

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
#from drf_haystack.viewsets import HaystackViewSet
#from drf_haystack.mixins import FacetMixin 
#from drf_haystack.filters import HaystackFacetFilter, HaystackFilter

from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.urls import reverse

from . import models
from . import serializers

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

class ListView(TemplateView):

    template_name = 'webflow/infrastructure-search.html'

    def get_context_data(self, **kwargs):
        view = ProjectViewSet.as_view({"get" : "list"}) 
        api_url = reverse("project-list")
        self.request.path = api_url

        projects = view(self.request, **kwargs).render().content
        projects = json.loads(projects)

        projects["view"] = "list";

        context = super().get_context_data(**kwargs)
        context['page_data_json'] = {"data" : json.dumps(projects)}
        return context

class DetailView(TemplateView):

    template_name = 'webflow/infrastructure-project.html'

    def get_full_serialize_url(self, pk):
        api_url = reverse("project-detail", args=(pk,))
        return "%s?full" % api_url

    def get_context_data(self, **kwargs):
        view = ProjectViewSet.as_view({"get" : "retrieve"}) 
        self.request.path = self.get_full_serialize_url(kwargs["pk"])

        project = view(self.request, **kwargs).render().content
        project = json.loads(project)

        project["view"] = "detail";

        context = super().get_context_data(**kwargs)
        context['page_data_json'] = {"data" : json.dumps(project)}
        return context

class FilterOrderMixin(object):
    def filter_queryset(self, request, queryset, view, *args, **kwargs):
        queryset = super(FilterOrderMixin, self).filter_queryset(
            request, queryset, view, *args, **kwargs
        )
        text_query = request.query_params.get("q", None)
        ordering = request.query_params.get("ordering", None)

        if text_query:
            queryset = queryset.filter(text=text_query)

        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset


#class ProjectFilter(FilterOrderMixin, HaystackFilter):
#    pass

#class ProjectFacetFilter(FilterOrderMixin, HaystackFacetFilter):
#    pass 

#class ProjectSearchView(FacetMixin, HaystackViewSet):
#
#    serializer_class = serializers.ProjectSearchSerializer
#    facet_serializer_class = serializers.ProjectFacetSerializer
#
#    facet_filter_backends = [ProjectFacetFilter]
#    filter_backends = [ProjectFilter]
#
#    def get_queryset(self):
#        print("B" * 100)
#        qs = super(ProjectSearchView, self).get_queryset()
#        return qs
#        print(qs)
#        raise Exception("ProjectSearchView " + "#" * 100)

