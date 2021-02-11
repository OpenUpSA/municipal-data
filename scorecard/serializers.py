from rest_framework import serializers

from municipal_finance.models import DemarcationChanges
from . import models
import municipal_finance
import decimal

import json

class GeographySerializer(serializers.ModelSerializer):
    bbox = serializers.SerializerMethodField()
    is_disestablished = serializers.SerializerMethodField('get_disestablished_status')

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

    def get_disestablished_status(self, obj):
        result = DemarcationChanges.objects.filter(old_code=obj.geo_code).values('old_code_transition')[:1]
        if result.exists():
            return "disestablished"
        else:
            return ""



class MunicipalityProfileSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        data = instance.data
        data["demarcation"]["code"] = instance.demarcation_code
        return data


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, models.Geography):
            return o.as_dict()
        return json.JSONEncoder.default(self, o)
