from django.conf.urls import include, url
from .. import views

urlpatterns = [
    url(r'^projects$', views.ListView.as_view(), name='project-list-view'),
]

