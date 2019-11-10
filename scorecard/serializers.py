from rest_framework import serializers
from . import models

class GeographySerializer(serializers.ModelSerializer):
    bbox = serializers.ReadOnlyField()

    class Meta:
        model = models.Geography
        exclude = ["id"]


