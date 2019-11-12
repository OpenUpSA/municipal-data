from haystack import indexes

from . import models


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    geography = indexes.CharField(model_attr="geography")
    province = indexes.CharField(faceted=True)
    geography_name = indexes.CharField(faceted=True)
    geo_code = indexes.CharField(faceted=True)
    geo_parent = indexes.CharField(faceted=True)

    function = indexes.CharField(model_attr="function", faceted=True)
    project_description = indexes.CharField(model_attr="project_description")
    project_number = indexes.CharField(model_attr="project_number")
    project_type = indexes.CharField(model_attr="project_type", faceted=True)
    mtsf_service_outcome = indexes.CharField(model_attr="mtsf_service_outcome")
    iudf = indexes.CharField(model_attr="iudf")
    own_strategic_objectives = indexes.CharField(model_attr="own_strategic_objectives")
    asset_class = indexes.CharField(model_attr="asset_class", faceted=True)
    asset_subclass = indexes.CharField(model_attr="asset_subclass", faceted=True)
    ward_location = indexes.CharField(model_attr="ward_location")

    def get_model(self):
        return models.Project

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_province(self, obj):
        return obj.geography.province_name

    def prepare_geography_name(self, obj):
        return obj.geography.name

    def prepare_geo_code(self, obj):
        return obj.geography.geo_code

    def prepare_geo_parent(self, obj):
        return obj.geography.parent_code
