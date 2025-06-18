import json
import csv

from django.views.generic.base import TemplateView
from django.urls import reverse
from django.contrib.postgres.search import SearchQuery
from constance import config

from . import models
from . import api as api_views
from django.http import HttpResponse
from infrastructure.utils import chart_quarters
from municipal_finance import settings


class ListView(TemplateView):
    if settings.SCORECARD_MAINTENANCE:
        template_name = "infrastructure/search-maintenance.djhtml"
    else:
        template_name = "infrastructure/search.djhtml"

    def get_context_data(self, **kwargs):
        view = api_views.ProjectViewSet.as_view({"get": "list"})
        api_url = reverse("project-list")
        self.request.path = api_url

        projects = view(self.request, **kwargs).render().content
        projects = json.loads(projects)

        projects["view"] = "list"
        projects["summary_year"] = config.CAPITAL_PROJECT_SUMMARY_YEAR

        context = super().get_context_data(**kwargs)
        context["page_data_json"] = {"data": json.dumps(projects)}

        context["page_title"] = "Infrastructure Projects - Municipal Money"
        context["page_description"]= "Infrastructure project search"

        return context


class DetailView(TemplateView):

    template_name = "infrastructure/project.djhtml"

    def get_full_serialize_url(self, pk):
        api_url = reverse("project-detail", args=(pk,))
        return "%s?full" % api_url

    def get_context_data(self, **kwargs):
        view = api_views.ProjectViewSet.as_view({"get": "retrieve"})
        self.request.path = self.get_full_serialize_url(kwargs["pk"])

        project = view(self.request, **kwargs).render().content
        project = json.loads(project)

        project["view"] = "detail"
        project["summary_year"] = config.CAPITAL_PROJECT_SUMMARY_YEAR

        context = super().get_context_data(**kwargs)
        context["page_data_json"] = {"data": json.dumps(project)}

        context["implementation_year"] = project["latest_implementation_year"][
            "budget_year"
        ]
        year = models.FinancialYear.objects.get(
            budget_year=context["implementation_year"]
        )

        project_quarters = models.ProjectQuarterlySpend.objects.filter(
            project__id=kwargs["pk"], financial_year=year
        )

        project_phases = models.Expenditure.objects.filter(
            project__id=kwargs["pk"], financial_year=year
        )

        (
            context["original_data"],
            context["adjusted_data"],
            context["quarter_data"],
        ) = chart_quarters(project_quarters, project_phases)

        is_quarters = False
        if project_quarters:
            is_quarters = True
        context["is_quarters"] = is_quarters

        context["page_title"] = f"{project['project_description']} - {project['geography']['name']} - Municipal Money"
        context["page_description"]= "Infrastructure project details"

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

    base_queryset = models.Project.objects.prefetch_related(
        "geography",
        "expenditure",
        "expenditure__financial_year",
        "expenditure__budget_phase",
    )
    queryset = filters(base_queryset, request.GET, annual_fieldmap)
    queryset = text_search(queryset, request.GET.get("q", ""))

    queryset = queryset | filters(base_queryset, request.GET, quarterly_fieldmap)
    queryset = text_search(queryset, request.GET.get("q", ""))

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
    ).distinct("project_number"):
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


def filters(qs, params, filter_map):
    query_dict = {}
    for k, v in filter_map.items():
        if v in params:
            query_dict[k] = params[v]
    return qs.filter(**query_dict)


def text_search(qs, text):
    if len(text) == 0:
        return qs

    return qs.filter(content_search=SearchQuery(text))
