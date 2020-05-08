from django.shortcuts import render
from django.views.generic.base import TemplateView


class PerformanceView(TemplateView):
    """
    Show all the indicators for a particular metro
    """

    template_name = "metro/municipality_performance.djhtml"
