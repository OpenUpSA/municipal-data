from django.conf.urls import url
from django.conf.urls import include
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
    url("admin/", admin.site.urls),
    url(r"^$", views.HomePage.as_view(), name="homepage"),
    url(r"^about", lambda request: redirect("/")),
    url(r"^faq", lambda request: redirect("/help")),
    url(r"^help$", views.HelpPage.as_view(), name="help"),
    url(r"^terms$", TemplateView.as_view(
        template_name="webflow/terms.html"), name="terms"),
    url(r"^sitemap.txt", views.SitemapView.as_view(), name="sitemap"),
    # e.g. /profiles/province-GT/
    url(
        regex="^profiles/(?P<geography_id>\w+-\w+)(-(?P<slug>[\w-]+))?/$",
        view=cache_page(CACHE_SECS)(views.GeographyDetailView.as_view()),
        kwargs={},
        name="geography_detail",
    ),
    url(
        regex="^profiles/(?P<geography_id>\w+-\w+)(-(?P<slug>[\w-]+))?\.pdf$",
        view=cache_page(CACHE_SECS)(views.GeographyPDFView.as_view()),
        kwargs={},
        name="geography_pdf",
    ),
    url(
        regex="^locate/$",
        view=cache_page(CACHE_SECS)(views.LocateView.as_view()),
        kwargs={},
        name="locate",
    ),
    url(
        regex="^robots.txt$",
        view=lambda r: HttpResponse(
            "User-agent: *\nAllow: /\n"
            "Crawl-Delay: 120 \n"
            + "Sitemap: https://municipalmoney.gov.za/sitemap.txt",
            content_type="text/plain",
        ),
    ),
    url(r"^favicon\.ico$", RedirectView.as_view(url="/static/images/favicon.ico")),
    url("^api/v1/infrastructure/", include("infrastructure.urls.api")),
    url("^infrastructure/", include("infrastructure.urls.templates")),
    url("^api/", include(router.urls)),
    url("^sentry-debug/", trigger_error),
    url('__debug__/', include(debug_toolbar.urls)),
]
