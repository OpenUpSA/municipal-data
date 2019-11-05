from django.conf.urls import url
from django.conf.urls import include
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from rest_framework import routers

import scorecard.views as views
import infrastructure.views

router = routers.DefaultRouter()
router.register(r'geography', views.GeographyViewSet)

urlpatterns = router.urls

# This cache is reset on each deployment. Corresponding caching headers are
# sent to the client, too.
CACHE_SECS = 12 * 60 * 60

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    url(r'^about', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^faq', TemplateView.as_view(template_name='faq.html'), name='faq'),
    url(r'^terms', TemplateView.as_view(template_name='terms.html'), name='terms'),
    url(r'^sitemap.txt', views.SitemapView.as_view(), name='sitemap'),
    # e.g. /profiles/province-GT/
    url(
        regex   = '^profiles/(?P<geography_id>\w+-\w+)(-(?P<slug>[\w-]+))?/$',
        view    = cache_page(CACHE_SECS)(views.GeographyDetailView.as_view()),
        kwargs  = {},
        name    = 'geography_detail',
    ),
    url(
        regex   = '^profiles/(?P<geography_id>\w+-\w+)(-(?P<slug>[\w-]+))?\.pdf$',
        view    = cache_page(CACHE_SECS)(views.GeographyPDFView.as_view()),
        kwargs  = {},
        name    = 'geography_pdf',
    ),
    # e.g. /compare/province-GT/vs/province-WC/
    url(
        regex   = '^compare/(?P<geo_id1>\w+-\w+)/vs/(?P<geo_id2>\w+-\w+)/$',
        view    = cache_page(CACHE_SECS)(views.GeographyCompareView.as_view()),
        kwargs  = {},
        name    = 'geography_compare',
    ),
    url(
        regex   = '^locate/$',
        view    = cache_page(CACHE_SECS)(views.LocateView.as_view()),
        kwargs  = {},
        name    = 'locate',
    ),
    url(
        regex='^robots.txt$',
        view=lambda r: HttpResponse(
            "User-agent: *\nAllow: /\n" +
            "Sitemap: https://municipalmoney.gov.za/sitemap.txt",
            content_type="text/plain"
        )
    ),
    url(
        '^api/infrastructure/', include("infrastructure.urls.api")
    ),
    url(
        '^infrastructure/', include("infrastructure.urls.templates")
    ),
    url(
        '^api/geography/', include(router.urls)
    ),
    url(
        regex='^api(?:/.*)?$',
        view=lambda r: HttpResponse(
            "The API is at https://municipaldata.treasury.gov.za/api\n" +
            "The API Documentation is at https://municipaldata.treasury.gov.za/docs\n",
            content_type="text/plain",
            status=404
        )
    ),
]
