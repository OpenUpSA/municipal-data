from rest_framework import serializers
from . import models

class GeographySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Geography
        exclude = ["id"]


