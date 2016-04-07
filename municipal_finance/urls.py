from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^status$', views.status),
    url(r'^cubes$', views.cubes),
    url(r'^cubes/(?P<cube_name>[\w_]+)/model$', views.model),
    url(r'^cubes/(?P<cube_name>[\w_]+)/aggregate$', views.aggregate),
    url(r'^cubes/(?P<cube_name>[\w_]+)/facts$', views.facts),
    url(r'^cubes/(?P<cube_name>[\w_]+)/members/(?P<member_ref>[\w_]+)$', views.members),
]
