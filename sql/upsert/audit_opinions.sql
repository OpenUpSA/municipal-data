BEGIN;

CREATE TEMPORARY TABLE audit_opinions_upsert
(
        demarcation_code TEXT,
        financial_year integer,
        opinion_code TEXT,
        opinion_label TEXT
) ON COMMIT DROP;

\copy audit_opinions_upsert (demarcation_code, financial_year, opinion_code, opinion_label) FROM '/home/jdb/proj/code4sa/municipalmoney/django-project/audit_opinions.csv' DELIMITER ',' CSV HEADER;

UPDATE audit_opinion_facts f
SET opinion_code = i.opinion_code,
    opinion_label = i.opinion_label
FROM audit_opinions_upsert i
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
FROM audit_opinions_upsert i
WHERE
    NOT EXISTS (
        SELECT * FROM audit_opinion_facts f
        WHERE f.demarcation_code = i.demarcation_code
        AND f.financial_year = i.financial_year
    );

COMMIT;
