from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

# Used to cache expensive API calls, since our data only changes occasionally
# This cache is reset on each deployment. Corresponding caching headers are
# sent to the client, too.
API_CACHE_SECS = 12 * 60 * 60

urlpatterns = [
    url(r'^$', cache_page(API_CACHE_SECS)(views.index)),
    url(r'^docs$', views.docs),
    url(r'^explore/(?P<cube_name>[\w_]+)/embed.html$', views.embed),
    url(r'^explore/(?P<cube_name>[\w_]+)/$', views.explore),
    url(r'^api/status$', views.status),
    url(r'^api/cubes$', cache_page(API_CACHE_SECS)(views.cubes)),
    url(r'^api/cubes/(?P<cube_name>[\w_]+)/model$', cache_page(API_CACHE_SECS)(views.model)),
    url(r'^api/cubes/(?P<cube_name>[\w_]+)/aggregate$', cache_page(API_CACHE_SECS)(views.aggregate)),
    url(r'^api/cubes/(?P<cube_name>[\w_]+)/facts$', cache_page(API_CACHE_SECS)(views.facts)),
    url(r'^api/cubes/(?P<cube_name>[\w_]+)/members/(?P<member_ref>[\w_.]+)$', cache_page(API_CACHE_SECS)(views.members)),
]
