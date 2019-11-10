from django.conf.urls import include, url
from .. import views

urlpatterns = [
    url(r'^projects/$', views.ListView.as_view(), name='project-list-view'),
    url(r'^projects/(?P<pk>\d+)/$', views.DetailView.as_view(), name='project-detail-view'),
    url(r'^search/', include('haystack.urls')),
]

