from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^cubes$', views.cubes),
    url(r'^cubes/(?P<cube_name>[\w_]+)/model$', views.model),
    # url(r'^cubes/<name>/aggregate$', views.agregate),
    url(r'^cubes/(?P<cube_name>[\w_]+)/facts$', views.facts),
    # url(r'^cubes/<name>/members/<ref>$', views.members),
]
