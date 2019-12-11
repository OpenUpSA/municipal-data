import json

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import ProjectDocument

class ProjectDocumentSerializer(DocumentSerializer):
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return int(obj.meta.id)

    class Meta(object):

        document = ProjectDocument
        fields = (
            "project_description",
            "project_number",
            "function",
            "project_type",
            "province",
            "municipality",
            "mtsf_service_outcome",
            "iudf",
            "own_strategic_objectives",
            "asset_class",
            "asset_subclass",
            "ward_location",
            "total_forecast_budget",
            "longitude",
            "latitude",
        )
