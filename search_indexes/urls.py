from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .viewsets import ProjectDocumentView
from . import views


router = DefaultRouter()
projects = router.register(r"projects",
    ProjectDocumentView,
    basename="projectdocument"
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'new_search/', views.ProjectView.as_view()),
]
