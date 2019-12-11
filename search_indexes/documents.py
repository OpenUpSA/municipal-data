from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from infrastructure.models import Project

budget_phase = fields.ObjectField(properties={
   "code": fields.TextField(),
   "name": fields.TextField()
})

financial_year = fields.ObjectField(properties={
   "budget_year": fields.TextField(),
})


@registry.register_document
class ProjectDocument(Document):

    #geography = fields.ObjectField(properties={
    #    "name": fields.TextField(),
    #    "province_name": fields.TextField(),
    #})

    #expenditure = fields.NestedField(properties={
    #    "budget_phase": budget_phase,
    #    "financial_year": financial_year,
    #    "amount": fields.DoubleField(),
    #})


    project_description = fields.KeywordField()
    project_type = fields.KeywordField()
    function = fields.KeywordField()
    province = fields.KeywordField()
    municipality = fields.KeywordField()

    # TODO year currently hardcoded - need to figure out the best way to handle this
    total_forecast_budget = fields.DoubleField()
    #id = fields.IntegerField(attr='id')
    def prepare_total_forecast_budget(self, instance):

        qs = instance.expenditure.filter(financial_year__budget_year="2019/2020")
        if qs.count() > 0:
            return qs.first().amount
        return 0

    def prepare_province(self, instance):
        return instance.geography.province_name

    def prepare_municipality(self, instance):
        return instance.geography.name

    def prepare_project_type(self, instance):
        return instance.project_type

    def get_queryset(self):
        # TODO remove slice - used for dev only
        return (super(ProjectDocument, self)
            .get_queryset()
            .select_related("geography")
            .prefetch_related("expenditure__budget_year", "expenditure__financial_Year")
        )

    class Index:
        # Name of the Elasticsearch index
        name = "projects"
        # See Elasticsearch Indices API reference for available settings
        settings = {"number_of_shards": 1,
                    "number_of_replicas": 0}

    class Django:
        model = Project 

        fields = [
            #"id",
            #"project_description",
            "project_number",
            "mtsf_service_outcome",
            "iudf",
            "own_strategic_objectives",
            "asset_class",
            "asset_subclass",
            "ward_location",
            "longitude",
            "latitude",
        ]
