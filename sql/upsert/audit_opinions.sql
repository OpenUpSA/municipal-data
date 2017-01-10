BEGIN;

CREATE TEMPORARY TABLE audit_reports_upsert
(
        demarcation_code TEXT,
        financial_year integer,
        url TEXT
) ON COMMIT DROP;

\copy audit_reports_upsert (demarcation_code, financial_year, url) FROM '/home/jdb/proj/code4sa/municipal_finance/django-app/reports_combined.csv' DELIMITER ',' CSV HEADER;

UPDATE audit_opinion_facts f
SET report_url = i.url
FROM audit_reports_upsert i
WHERE f.demarcation_code = i.demarcation_code
AND f.financial_year = i.financial_year
and f.report_url != i.url;

COMMIT;
