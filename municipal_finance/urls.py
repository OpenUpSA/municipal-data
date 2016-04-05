from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^cubes$', views.cubes),
    url(r'^cubes/(?P<cube_name>[\w_]+)/model$', views.model),
    url(r'^cubes/(?P<cube_name>[\w_]+)/aggregate$', views.aggregate),
    url(r'^cubes/(?P<cube_name>[\w_]+)/facts$', views.facts),
    url(r'^cubes/(?P<cube_name>[\w_]+)/members/(?P<member_ref>[\w_]+)$', views.members),
]
