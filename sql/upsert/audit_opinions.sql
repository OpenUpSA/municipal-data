BEGIN;

CREATE TEMPORARY TABLE audit_opinions_2015q4
(
        demarcation_code TEXT,
        financial_year integer,
        opinion_code TEXT,
        opinion_label TEXT
) ON COMMIT DROP;

\copy audit_opinions_2015q4 (demarcation_code, financial_year, opinion_code, opinion_label) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/non-financial/audit_opinions_2016.csv' DELIMITER ',' CSV HEADER;

UPDATE audit_opinion_facts f
SET opinion_code = i.opinion_code,
    opinion_label = i.opinion_label
FROM audit_opinions_2015q4 i
WHERE f.demarcation_code = i.demarcation_code
AND f.financial_year = i.financial_year
and f.opinion_code != i.opinion_code;

INSERT INTO audit_opinion_facts
(
    demarcation_code,
    financial_year,
    opinion_code,
    opinion_label
)
SELECT demarcation_code, financial_year, opinion_code, opinion_label
FROM audit_opinions_2015q4 i
WHERE
    NOT EXISTS (
        SELECT * FROM audit_opinion_facts f
        WHERE f.demarcation_code = i.demarcation_code
        AND f.financial_year = i.financial_year
    );

UPDATE audit_opinion_facts f
SET report_url = i.report_url
FROM audit_report_import i
WHERE f.demarcation_code = i.demarcation_code
AND f.financial_year = i.financial_year::integer;

COMMIT;
