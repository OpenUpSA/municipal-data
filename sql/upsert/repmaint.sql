\set ON_ERROR_STOP on

BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE repmaint_upsert
(
        demarcation_code TEXT,
        period_code TEXT,
        item_code TEXT,
        amount DECIMAL
) ON COMMIT DROP;

\echo Read data...

\copy repmaint_upsert (demarcation_code, period_code, item_code, amount) FROM '/data/Section 71 Q3 2018-19/rm_2019q3_acrmun.csv' DELIMITER ',' CSV HEADER;

\echo Delete demarcation_code-period_code pairs that are in the update

DELETE FROM repmaint_facts f WHERE EXISTS (
        SELECT 1 FROM repmaint_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        LIMIT 1
    );

\echo Insert new values...

INSERT INTO repmaint_facts
(
    demarcation_code,
    period_code,
    item_code,
    amount,
    financial_year,
    amount_type_code,
    period_length,
    financial_period
)
SELECT demarcation_code,
       period_code,
       item_code,
       amount,
       cast(left(period_code, 4) as int),
       case when substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD')
               then substr(period_code, 5)
           when period_code ~ '\d{4}M\d{2}'
               then 'ACT'
       end,
       case when period_code ~ '\d{4}M\d{2}'
                then 'month'
            when period_code ~ '\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD)'
                then 'year'
       end,
       case when period_code ~ '\d{4}M\d{2}'
                then cast(right(period_code, 2) as int)
            when period_code ~ '\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD)'
                then cast(left(period_code, 4) as int)
       end
FROM repmaint_upsert i;

COMMIT;
