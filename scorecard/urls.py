from django.conf.urls import url
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from wazimap.views import GeographyDetailView, PlaceSearchJson

import scorecard.views as views

# This cache is reset on each deployment. Corresponding caching headers are
# sent to the client, too.
CACHE_SECS = 12 * 60 * 60

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='homepage'),

    # e.g. /profiles/province-GT/
    url(
        regex   = '^profiles/(?P<geography_id>\w+-\w+)(-(?P<slug>[\w-]+))?/$',
        view    = cache_page(CACHE_SECS)(GeographyDetailView.as_view()),
        kwargs  = {},
        name    = 'geography_detail',
    ),
    url(
        regex   = '^profiles/(?P<geography_id>\w+-\w+)(-(?P<slug>[\w-]+))?\.pdf$',
        view    = cache_page(CACHE_SECS)(views.GeographyPDFView.as_view()),
        kwargs  = {},
        name    = 'geography_pdf',
    ),
    url(
        regex   = '^place-search/json/$',
        view    = cache_page(CACHE_SECS)(PlaceSearchJson.as_view()),
        kwargs  = {},
        name    = 'place_search_json',
    ),
    url(
        regex   = '^locate/$',
        view    = cache_page(CACHE_SECS)(views.locate),
        kwargs  = {},
        name    = 'locate',
    ),
]
