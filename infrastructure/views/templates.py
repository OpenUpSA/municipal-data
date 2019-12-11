import json

from django.views.generic.base import TemplateView
from django.urls import reverse

from . import models
from . import api as api_views

class ListView(TemplateView):

    template_name = 'webflow/infrastructure-search.html'

    def get_context_data(self, **kwargs):
        view = api_views.ProjectViewSet.as_view({"get" : "list"}) 
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
        view = api_views.ProjectViewSet.as_view({"get" : "retrieve"}) 
        self.request.path = self.get_full_serialize_url(kwargs["pk"])

        project = view(self.request, **kwargs).render().content
        project = json.loads(project)

        project["view"] = "detail";

        context = super().get_context_data(**kwargs)
        context['page_data_json'] = {"data" : json.dumps(project)}
        return context

