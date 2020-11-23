# The years for which we need results. Must be in desceneding order.
LAST_AUDIT_YEAR = 2019
LAST_AUDIT_QUARTER = "2019q4"
YEARS = list(range(LAST_AUDIT_YEAR - 3, LAST_AUDIT_YEAR + 1))
YEARS.reverse()

LAST_OPINION_YEAR = 2019
AUDIT_OPINION_YEARS = list(range(LAST_OPINION_YEAR - 3, LAST_OPINION_YEAR + 1))
AUDIT_OPINION_YEARS.reverse()

# we'll actually only have data up to the year before this but use four
# for consistency on the page.
LAST_UIFW_YEAR = 2019
UIFW_YEARS = list(range(LAST_UIFW_YEAR - 3, LAST_UIFW_YEAR + 1))
UIFW_YEARS.reverse()

LAST_IN_YEAR_YEAR = 2019
IN_YEAR_YEARS = [
    LAST_IN_YEAR_YEAR + 1,
    LAST_IN_YEAR_YEAR,
    LAST_IN_YEAR_YEAR - 1,
    LAST_IN_YEAR_YEAR - 2,
]
