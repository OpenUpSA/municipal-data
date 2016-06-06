update audit_opinion_facts f
set report_url = i.report_url
from audit_report_import i
where f.demarcation_code = i.demarcation_code
and f.financial_year = i.financial_year;
