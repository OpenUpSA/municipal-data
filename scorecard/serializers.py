from rest_framework import serializers
from . import models

import json

class GeographySerializer(serializers.ModelSerializer):
    bbox = serializers.SerializerMethodField()

    def get_bbox(self, obj):
        if "full" in self.context:
            return obj.bbox
        elif "request" in self.context and self.context["request"] is not None:
            if "full" in self.context["request"]._request.path:
                return obj.bbox
        return []

    class Meta:
        model = models.Geography
        exclude = ["id"]


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, models.Geography):
            return o.as_dict()
        return json.JSONEncoder.default(self, o)
