import json
import csv

from django.views.generic.base import TemplateView
from django.urls import reverse
from django.contrib.postgres.search import SearchQuery
from . import models
from . import api as api_views
from django.http import HttpResponse


class ListView(TemplateView):

    template_name = "webflow/infrastructure-search.html"

    def get_context_data(self, **kwargs):
        view = api_views.ProjectViewSet.as_view({"get": "list"})
        api_url = reverse("project-list")
        self.request.path = api_url

        projects = view(self.request, **kwargs).render().content
        projects = json.loads(projects)

        projects["view"] = "list"

        context = super().get_context_data(**kwargs)
        context["page_data_json"] = {"data": json.dumps(projects)}
        return context


class DetailView(TemplateView):

    template_name = "webflow/infrastructure-project.html"

    def get_full_serialize_url(self, pk):
        api_url = reverse("project-detail", args=(pk,))
        return "%s?full" % api_url

    def get_context_data(self, **kwargs):
        view = api_views.ProjectViewSet.as_view({"get": "retrieve"})
        self.request.path = self.get_full_serialize_url(kwargs["pk"])

        project = view(self.request, **kwargs).render().content
        project = json.loads(project)

        project["view"] = "detail"

        context = super().get_context_data(**kwargs)
        context["page_data_json"] = {"data": json.dumps(project)}
        return context


def download_csv(request):
    """
    Downloads csv of all the projects
    """
    response = HttpResponse(content_type="text/csv")
    file_name = "infrastructure_projects.csv"
    response["Content-Disposition"] = f"attachment;filename={file_name}"
    csv_fields = [
        "province",
        "municipality",
        "project_number",
        "project_description",
        "project_type",
        "function",
        "asset_class",
        "mtsf_service_outcome",
        "own_strategic_objectives",
        "iudf",
        "budget phase",
        "financial year",
        "amount",
        "latitude",
        "longitude",
    ]

    queryset = models.Project.objects.prefetch_related(
        "geography",
        "expenditure",
        "expenditure__financial_year",
        "expenditure__budget_phase",
    )
    queryset = filters(queryset, request.GET)
    queryset = text_search(queryset, request.GET.get("q", ""))
    queryset = queryset.order_by("expenditure__amount")

    writer = csv.DictWriter(response, fieldnames=csv_fields)
    writer.writeheader()
    for project in queryset.values(
        "geography__province_name",
        "geography__name",
        "project_number",
        "project_description",
        "project_type",
        "function",
        "asset_class",
        "mtsf_service_outcome",
        "own_strategic_objectives",
        "iudf",
        "expenditure__budget_phase__name",
        "expenditure__financial_year__budget_year",
        "expenditure__amount",
        "latitude",
        "longitude",
    ):
        # budget_phase = request.GET.get("budget_phase", "Budget year")
        # financial_year = request.GET.get("financial_year", "2019/2020")
        # try:
        #     expenditure = project.expenditure.get(
        #         budget_phase__name=budget_phase,
        #         financial_year__budget_year=financial_year,
        #     )
        # except models.Expenditure.DoesNotExist:
        #     continue

        writer.writerow(
            {
                "province": project["geography__province_name"],
                "municipality": project["geography__name"],
                "project_number": project["project_number"],
                "project_description": project["project_description"],
                "project_type": project["project_type"],
                "function": project["function"],
                "asset_class": project["asset_class"],
                "mtsf_service_outcome": project["mtsf_service_outcome"],
                "own_strategic_objectives": project["own_strategic_objectives"],
                "iudf": project["iudf"],
                "budget phase": project["expenditure__budget_phase__name"],
                "financial year": project["expenditure__financial_year__budget_year"],
                "amount": project["expenditure__amount"],
                "latitude": project["latitude"],
                "longitude": project["longitude"],
            }
        )

    return response


def filters(queryset, params):
    fieldmap = {
        "function": "function",
        "project_type": "project_type",
        "municipality": "geography__name",
        "province": "geography__province_name",
        "budget_phase": "expenditure__budget_phase__name",
        "financial_year": "expenditure__financial_year__budget_year",
    }
    query_dict = {}
    for k, v in fieldmap.items():
        if k in params:
            query_dict[v] = params[k]

    return queryset.filter(**query_dict)


def text_search(qs, text):
    if len(text) == 0:
        return qs

    return qs.filter(content_search=SearchQuery(text))
