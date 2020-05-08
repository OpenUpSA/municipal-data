from django.conf.urls import url

from . import views

urlpatterns = (
    url(
        r"^performance/(?P<geography_id>\w+-\w+)(-(?P<slug>[\w-]+))?/$",
        views.PerformanceView.as_view(),
    ),
)
