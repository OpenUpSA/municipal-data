from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^cubes$', views.cubes),
    url(r'^cubes/<name>/model$', views.model),
    url(r'^cubes/<name>/aggregate$', views.agregate),
    url(r'^cubes/<name>/facts$', views.facts),
    url(r'^cubes/<name>/members/<ref>$', views.members),
]
