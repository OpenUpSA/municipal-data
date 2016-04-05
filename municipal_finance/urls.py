from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^cubes$', views.cubes),
    # (?P<site_slug>[\w-]+)
    url(r'^cubes/(?P<cube_name>[\w_]+)/model$', views.model),
    # url(r'^cubes/<name>/aggregate$', views.agregate),
    # url(r'^cubes/<name>/facts$', views.facts),
    # url(r'^cubes/<name>/members/<ref>$', views.members),
]
