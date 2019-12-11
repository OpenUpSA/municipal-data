from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .viewsets import ProjectDocumentView


router = DefaultRouter()
projects = router.register(r"projects",
    ProjectDocumentView,
    basename="projectdocument"
)

urlpatterns = [
    url(r'^', include(router.urls)),
]
