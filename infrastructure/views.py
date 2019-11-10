import json

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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

    def get_context_data(self, **kwargs):
        view = ProjectViewSet.as_view({"get" : "retrieve"}) 
        api_url = reverse("project-detail", args=(kwargs["pk"],))
        self.request.path = api_url

        project = view(self.request, **kwargs).render().content
        project = json.loads(project)

        print(kwargs)
        context = super().get_context_data(**kwargs)
        context['page_data_json'] = {"data" : json.dumps(project)}
        return context
