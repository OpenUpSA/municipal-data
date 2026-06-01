from django.urls import re_path, include
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView
from django.contrib import admin
from django.http import HttpResponse

from . import views


# This cache is reset on each deployment. Corresponding caching headers are
# sent to the client, too.
API_CACHE_SECS = 5 * 60  # 5 minutes

urlpatterns = [
    re_path("admin/", admin.site.urls),
    re_path(r"^$", cache_page(API_CACHE_SECS)(views.index), name="homepage"),
    re_path(r"^docs$", cache_page(API_CACHE_SECS)(views.docs)),
    re_path(
        r"^terms",
        RedirectView.as_view(
            url="https://municipalmoney.gov.za/terms", permanent=False
        ),
        name="termsa",
    ),
    re_path(r"^table/(?P<cube_name>[\w_]+)/$", views.table, name="table"),
    re_path(r"^api/?$", views.api_root),
    re_path(r"^api/status$", views.status),
    re_path(r"^api/cubes/?$", cache_page(API_CACHE_SECS)(views.cubes)),
    re_path(
        r"^api/cubes/(?P<cube_name>[\w_]+)/?$",
        cache_page(API_CACHE_SECS)(views.cube_root),
    ),
    re_path(
        r"^api/cubes/(?P<cube_name>[\w_]+)/model$",
        cache_page(API_CACHE_SECS)(views.model),
    ),
    re_path(
        r"^api/cubes/(?P<cube_name>[\w_]+)/aggregate$",
        cache_page(API_CACHE_SECS)(views.aggregate),
    ),
    re_path(
        r"^api/cubes/(?P<cube_name>[\w_]+)/facts$",
        cache_page(API_CACHE_SECS)(views.facts),
    ),
    re_path(
        r"^api/cubes/(?P<cube_name>[\w_]+)/members/?$",
        cache_page(API_CACHE_SECS)(views.members_root),
    ),
    re_path(
        r"^api/cubes/(?P<cube_name>[\w_]+)/members/(?P<member_ref>[\w_.]+)$",
        cache_page(API_CACHE_SECS)(views.members),
    ),
    re_path(
        r"^robots.txt$",
        lambda r: HttpResponse(
            "User-agent: *\nAllow: /\n"
            "Crawl-Delay: 120 \n"
            + "Sitemap: https://municipalmoney.gov.za/sitemap.txt",
            content_type="text/plain",
        ),
    ),
    re_path(r"^favicon\.ico$", RedirectView.as_view(url="/static/images/favicon.ico")),
]
