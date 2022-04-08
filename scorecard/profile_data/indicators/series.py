
class SeriesIndicator():

    @classmethod
    def get_muni_specifics(cls, api_data):
        results = api_data.results
        years = api_data.years
        return {
            "result_type": cls.result_type,
            "values": cls.get_values(years, results),
            "ref": api_data.references[cls.reference],
            "last_year": years[0] if len(years) > 0 else None,
            "formula": cls.formula,
        }