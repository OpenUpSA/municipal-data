#from elasticsearch_dsl import FacetedSearch, TermsFacet, A
#
#class ProjectSearch(FacetedSearch):
#    fields = ["project_description", "project_number", "mtsf_service_outcome", "iudf", "own_strategic_objectives", "asset_class", "asset_subclass"]
#    facets = {
#        "type": TermsFacet(field="project_type"),
#        "function": TermsFacet(field="function"),
#        "province": TermsFacet(field="province"),
#        "municipality": TermsFacet(field="municipality"),
#        "municipality_budget": TermsFacet(field="municipality", metric=(A("sum", field="total_forecast_budget"))),
#    }
#
#    def scan(self):
#        s = super().search()
#        return self._s.scan()
