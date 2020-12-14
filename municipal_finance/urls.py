from django.conf.urls import url
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from django.conf.urls import include
from django.contrib import admin

from . import views


# This cache is reset on each deployment. Corresponding caching headers are
# sent to the client, too.
API_CACHE_SECS = 5 * 60 # 5 minutes

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r"^$", cache_page(API_CACHE_SECS)(views.index), name="homepage"),
    url(r"^docs$", cache_page(API_CACHE_SECS)(views.docs)),
    url(r"^terms", TemplateView.as_view(template_name="terms.html"), name="terms"),
    url(r"^table/(?P<cube_name>[\w_]+)/$", views.table, name="table"),
    url(r"^api/?$", views.api_root),
    url(r"^api/status$", views.status),
    url(r"^api/cubes/?$", cache_page(API_CACHE_SECS)(views.cubes)),
    url(
        r"^api/cubes/(?P<cube_name>[\w_]+)/?$",
        cache_page(API_CACHE_SECS)(views.cube_root),
    ),
    url(
        r"^api/cubes/(?P<cube_name>[\w_]+)/model$",
        cache_page(API_CACHE_SECS)(views.model),
    ),
    url(
        r"^api/cubes/(?P<cube_name>[\w_]+)/aggregate$",
        cache_page(API_CACHE_SECS)(views.aggregate),
    ),
    url(
        r"^api/cubes/(?P<cube_name>[\w_]+)/facts$",
        cache_page(API_CACHE_SECS)(views.facts),
    ),
    url(
        r"^api/cubes/(?P<cube_name>[\w_]+)/members/?$",
        cache_page(API_CACHE_SECS)(views.members_root),
    ),
    url(
        r"^api/cubes/(?P<cube_name>[\w_]+)/members/(?P<member_ref>[\w_.]+)$",
        cache_page(API_CACHE_SECS)(views.members),
    ),
]
