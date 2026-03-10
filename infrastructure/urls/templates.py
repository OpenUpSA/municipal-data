from django.urls import re_path
from .. import views

urlpatterns = [
    re_path(r"^projects/$", views.ListView.as_view(), name="project-list-view"),
    re_path(
        r"^projects/(?P<pk>\d+)/$",
        views.DetailView.as_view(),
        name="project-detail-view",
    ),
    re_path(r"^download$", views.download_csv, name="download_csv"),
]
