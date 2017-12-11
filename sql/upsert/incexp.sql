\set ON_ERROR_STOP on

BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE incexp_upsert
(
        demarcation_code TEXT,
        period_code TEXT,
        function_code TEXT,
        item_code TEXT,
        amount DECIMAL
) ON COMMIT DROP;
CREATE INDEX incexp_upsert_demarcation_code on incexp_upsert (demarcation_code);
CREATE INDEX incexp_upsert_period_code on incexp_upsert (period_code);

\echo Read data...

\copy incexp_upsert (demarcation_code, period_code, function_code, item_code, amount) FROM '/home/jdb/proj/code4sa/municipalmoney/data/Section 71 Q1 2017-18/incexp_2018q1_acrmun.csv' DELIMITER ',' CSV HEADER;

\echo Delete demarcation_code-period_code pairs that are in the update

DELETE FROM incexp_facts f WHERE EXISTS (
        SELECT 1 FROM incexp_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        LIMIT 1
    );

\echo Insert new values...

INSERT INTO incexp_facts
(
    demarcation_code,
    period_code,
    function_code,
    item_code,
    amount,
    financial_year,
    amount_type_code,
    period_length,
    financial_period
)
SELECT demarcation_code,
       period_code,
       function_code,
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
FROM incexp_upsert i;

COMMIT;
