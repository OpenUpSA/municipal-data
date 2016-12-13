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

\copy cflow_upsert (demarcation_code, period_code, item_code, amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2016q4/cflow_2016q4_acrmun.csv' DELIMITER ',' CSV HEADER;

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
       case when substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD')
           then substr(period_code, 5)
           else 'ACT'
       end,
       case when substr(period_code, 5, 3) not similar to 'M\d{2}'
            then 'year'
            else 'month'
       end,
       case when substr(period_code, 5, 3) similar to 'M\d{2}'
            then cast(right(period_code, 2) as int)
            else cast(left(period_code, 4) as int)
       end
FROM cflow_upsert i;


COMMIT;
