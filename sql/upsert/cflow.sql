\set ON_ERROR_STOP on

BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE cflow_upsert
(
        demarcation_code TEXT,
        period_code TEXT,
        item_code TEXT,
        amount DECIMAL
) ON COMMIT DROP;

\echo Read data...

\copy cflow_upsert (demarcation_code, period_code, item_code, amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2017q1/cflow_2017q1_acrmun.csv' DELIMITER ',' CSV HEADER;

\echo Delete demarcation_code-period_code pairs that are in the update

DELETE FROM cflow_facts f WHERE EXISTS (
        SELECT 1 FROM cflow_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        LIMIT 1
    );

\echo Insert new values...

INSERT INTO cflow_facts
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
       case when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD)(M\d{2})?$'
               then substr(period_code, 5, 4)
           when period_code ~ '^\d{4}M\d{2}$'
               then 'ACT'
       end,
       case when period_code ~ '^\d{4}(ADJB|ORGB)?M\d{2}$'
                then 'month'
            when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD)$'
                then 'year'
       end,
       case when period_code ~ '^\d{4}(ADJB|ORGB)?M\d{2}$'
                then cast(right(period_code, 2) as int)
            when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD)$'
                then cast(left(period_code, 4) as int)
       end
FROM cflow_upsert i;

COMMIT;
