\set ON_ERROR_STOP on

BEGIN;

--  demarcation_code | text    | not null
--  financial_year   | integer | not null
--  item_code        | text    | not null
--  item_label       | text    | not null
--  amount           | bigint  |
--  id               | integer | not null default nextval('badexp_facts_id_seq'::regclass)

\echo Create import table...

CREATE TEMPORARY TABLE uifw_upsert
(
        demarcation_code TEXT,
        financial_year TEXT,
        item_code TEXT,
        item_label TEXT,
        amount DECIMAL
) ON COMMIT DROP;

\echo Read data...

\copy uifw_upsert (demarcation_code, financial_year, item_code, item_label, amount) FROM '/home/ubuntu/django-project/uifw-2015.csv' DELIMITER ',' CSV HEADER;

\echo Delete demarcation_code-financial_year pairs that are in the update

DELETE FROM uifwexp_facts f WHERE EXISTS (
        SELECT 1 FROM uifw_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.financial_year = i.financial_year::int
        LIMIT 1
    );

\echo Insert new values...

INSERT INTO uifwexp_facts
(
    demarcation_code,
    financial_year,
    item_code,
    item_label,
    amount
)
SELECT demarcation_code,
       financial_year::int,
       item_code,
       item_label,
       amount
FROM uifw_upsert i;

COMMIT;
