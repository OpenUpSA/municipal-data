from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^explore/(?P<cube_name>[\w_]+)/$', views.explore),
    url(r'^api/status$', views.status),
    url(r'^api/cubes$', views.cubes),
    url(r'^api/cubes/(?P<cube_name>[\w_]+)/model$', views.model),
    url(r'^api/cubes/(?P<cube_name>[\w_]+)/aggregate$', views.aggregate),
    url(r'^api/cubes/(?P<cube_name>[\w_]+)/facts$', views.facts),
    url(r'^api/cubes/(?P<cube_name>[\w_]+)/members/(?P<member_ref>[\w_.]+)$', views.members),
]
