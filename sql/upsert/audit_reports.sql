BEGIN;

CREATE TEMPORARY TABLE audit_reports_upsert
(
        demarcation_code TEXT,
        financial_year integer,
        url TEXT
) ON COMMIT DROP;

\copy audit_reports_upsert (demarcation_code, financial_year, url) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/non-financial/audit_reports.csv' DELIMITER ',' CSV HEADER;

UPDATE audit_opinion_facts f
SET report_url = i.url
FROM audit_reports_upsert i
WHERE f.demarcation_code = i.demarcation_code
AND f.financial_year = i.financial_year
and f.financial_year = 2016;

COMMIT;
