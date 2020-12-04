"""
Municipality Profile data preparation
-------------------------------------
Gather data from the municipal finance API and provide values ready for display
on the page with little further processing.

If the API returns a null value, it can generally be treated as zero. That
happens in this library and nulls that should be zeros should not be
left to the frontend to handle.

The shape of data produced by this library is generally a series of years
or quarters in reverse chronological order with associated values. Only the
years that are to be shown are returned.

If data needed to calculate a value for a given date is missing, an
object is returned for that year with the value being None,
to indicate in the page that it is missing.
"""

from itertools import groupby
import dateutil.parser

from .utils import (
    calendar_to_financial,
    quarter_string,
)

from .api_client import ApiClient
from .api_data import ApiData


class Demarcation(object):
    def __init__(self, api_data):
        self.land_gained = []
        self.land_lost = []
        self.disestablished = False
        self.established_after_last_audit = False
        self.established_within_audit_years = False
        def date_key(x): return x["date.date"]
        # Watch out: groupby's iterator is finicky about seeing things twice.
        # E.g. If you just turn the tuples iterator into a list you only see one
        # item in the group
        for date, group in groupby(api_data.results["disestablished"], date_key):
            if self.disestablished:
                # If this is the second iteration
                raise Exception("Muni disestablished more than once")
            else:
                self.disestablished = True
                self.disestablished_date = date
                self.disestablished_to = [
                    x["new_demarcation.code"] for x in group]
        for date, group in groupby(api_data.results["established"], date_key):
            if self.established_after_last_audit:
                # If this is the second iteration
                raise Exception("Muni established more than once")
            else:
                datetime = dateutil.parser.parse(date)
                year, month = calendar_to_financial(
                    datetime.year, datetime.month)
                quarter = quarter_string(year, month)
                if quarter > api_data.last_audit_quarter:
                    self.established_after_last_audit = True
                if datetime.year in api_data.years:
                    self.established_within_audit_years = True
                self.established_date = date
                self.established_from = [
                    x["old_demarcation.code"] for x in group]
        for date, group in groupby(
            api_data.results["demarcation_involved_new"], date_key
        ):
            self.land_gained.append(
                {
                    "date": date,
                    "changes": [
                        {
                            "change": x["old_code_transition.code"],
                            "demarcation_code": x["old_demarcation.code"],
                        }
                        for x in group
                    ],
                }
            )
        for date, group in groupby(
            api_data.results["demarcation_involved_old"], date_key
        ):
            self.land_lost.append(
                {
                    "date": date,
                    "changes": [
                        {
                            "change": x["new_code_transition.code"],
                            "demarcation_code": x["new_demarcation.code"],
                        }
                        for x in group
                    ],
                }
            )

    def as_dict(self):
        demarcation_dict = {
            "land_gained": self.land_gained,
            "land_lost": self.land_lost,
        }
        if self.disestablished:
            demarcation_dict.update(
                {
                    "disestablished": True,
                    "disestablished_date": self.disestablished_date,
                    "disestablished_to": self.disestablished_to,
                }
            )
        if self.established_after_last_audit or self.established_within_audit_years:
            demarcation_dict.update(
                {
                    "established_after_last_audit": self.established_after_last_audit,
                    "established_within_audit_years": self.established_within_audit_years,
                    "established_date": self.established_date,
                    "established_from": self.established_from,
                }
            )
        return demarcation_dict
