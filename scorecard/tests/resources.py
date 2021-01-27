
from import_export import resources

from municipal_finance.tests.resources import (
    MunicipalityProfileResource,
    MedianGroupResource,
    RatingCountGroupResource,
)
from ..models import Geography

class GeographyResource(resources.ModelResource):
    class Meta:
        model = Geography
        import_id_fields = ['geo_code']
