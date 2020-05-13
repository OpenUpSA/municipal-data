from django.shortcuts import render
from django.views.generic.base import TemplateView
from scorecard.models import Geography, LocationNotFound
from django.http import Http404
from django.shortcuts import redirect
from django.db.models import Q

from .models import Category, IndicatorQuarterResult, FinancialYear
from . import utils


class PerformanceView(TemplateView):
    """
    Show all the indicators for a particular metro
    """

    template_name = "metro/municipality_performance.djhtml"

    def dispatch(self, *args, **kwargs):
        self.geo_id = self.kwargs.get("geography_id", None)

        try:
            self.geo_level, self.geo_code = self.geo_id.split("-", 1)
            self.geo = Geography.find(self.geo_code, self.geo_level)
        except (ValueError, LocationNotFound):
            raise Http404

        # check slug
        if kwargs.get("slug") or self.geo.slug:
            if kwargs["slug"] != self.geo.slug:
                kwargs["slug"] = self.geo.slug
                url = "/metro/performance/%s-%s-%s/" % (
                    self.geo_level,
                    self.geo_code,
                    self.geo.slug,
                )
                return redirect(url, permanent=True)

        return super(PerformanceView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        page_context = {}
        page_context["geography"] = self.geo.as_dict()
        metros = Geography.objects.filter(
            parent_level="province", geo_level="municipality"
        )
        page_context["metros"] = metros

        category = (
            Category.objects.all().filter(~Q(name="Unknown")).only("name", "slug")
        )
        page_context["category"] = category

        quarter_results = IndicatorQuarterResult.objects.filter(
            indicator__tier="Tier 1",
            financial_year__active=True,
            geography__geo_code=self.geo_code,
        )

        current_quarter = FinancialYear.current_quarter()

        quarter_results_sort = utils.category_sort(quarter_results)
        page_context["quarter_results"] = quarter_results_sort

        page_context["current_quarter"] = current_quarter
        page_context["current_financial_year"] = FinancialYear.financial_year.active()
        return page_context
