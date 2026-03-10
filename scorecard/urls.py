from django.urls import re_path, include
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView
from rest_framework import routers
from django.contrib import admin
import debug_toolbar
from django.shortcuts import redirect
import scorecard.views as views
import infrastructure.views

router = routers.DefaultRouter()
router.register(r"geography/geography", views.GeographyViewSet)
router.register(r"municipality-profile", views.MunicipalityProfileViewSet)

# This cache is reset on each deployment. Corresponding caching headers are
# sent to the client, too.
CACHE_SECS = 2 * 60  # 2 minutes


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    re_path("admin/", admin.site.urls),
    re_path(r"^$", views.HomePage.as_view(), name="homepage"),
    re_path(r"^about", lambda request: redirect("/")),
    re_path(r"^faq", lambda request: redirect("/help")),
    re_path(r"^help$", views.HelpPage.as_view(), name="help"),
    re_path(r"^terms$", TemplateView.as_view(
        template_name="webflow/terms.html"), name="terms"),
    re_path(r"^sitemap.txt", views.SitemapView.as_view(), name="sitemap"),
    # e.g. /profiles/province-GT/
    re_path(
        r"^profiles/(?P<geography_id>\w+-\w+)(-(?P<slug>[\w-]+))?/$",
        cache_page(CACHE_SECS)(views.GeographyDetailView.as_view()),
        kwargs={},
        name="geography_detail",
    ),
    re_path(
        r"^profiles/(?P<geography_id>\w+-\w+)(-(?P<slug>[\w-]+))?\.pdf$",
        cache_page(CACHE_SECS)(views.GeographyPDFView.as_view()),
        kwargs={},
        name="geography_pdf",
    ),
    re_path(
        r"^locate/$",
        cache_page(CACHE_SECS)(views.LocateView.as_view()),
        kwargs={},
        name="locate",
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
    re_path("^api/v1/infrastructure/", include("infrastructure.urls.api")),
    re_path("^infrastructure/", include("infrastructure.urls.templates")),
    re_path("^api/", include(router.urls)),
    re_path("^sentry-debug/", trigger_error),
    re_path('__debug__/', include(debug_toolbar.urls)),
]
