\set ON_ERROR_STOP on

BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE capital_upsert
(
        demarcation_code TEXT,
        period_code TEXT,
        function_code TEXT,
        item_code TEXT,
        capital_type_code TEXT,
        amount DECIMAL
) ON COMMIT DROP;
CREATE INDEX capital_upsert_demarcation_code on capital_upsert (demarcation_code);
CREATE INDEX capital_upsert_period_code on capital_upsert (period_code);

\echo Read data...

\copy capital_upsert (demarcation_code, period_code, function_code, item_code, capital_type_code, amount) FROM '' DELIMITER ',' CSV HEADER;

\echo Delete demarcation_code-period_code pairs that are in the update

DELETE FROM capital_facts_v2 f WHERE EXISTS (
        SELECT 1 FROM capital_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        LIMIT 1
    );

\echo Insert new values...

INSERT INTO capital_facts_v2
(
    demarcation_code,
    period_code,
    function_id,
    item_id,
    capital_type_id,
    financial_year,
    amount_type_id,
    period_length,
    financial_period,
    amount
)
SELECT demarcation_code,
       period_code,
       (select id from government_functions_v2 where government_functions_v2.code = function_code),
       (select id from capital_items_v2 where capital_items_v2.code = item_code),
       (select id from capital_type_v2 where capital_type_v2.code = capital_type_code),
       cast(left(period_code, 4) as int),
       case when substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD', 'ITY1', 'ITY2', 'TABB')
               then (select id from amount_type_v2 where amount_type_v2.code = substr(period_code, 5))
           when period_code ~ '^\d{4}M\d{2}$'
               then (select id from amount_type_v2 where amount_type_v2.code = 'ACT')
       end,
       case when period_code ~ '^\d{4}M\d{2}$'
                then 'month'
            when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD|ITY1|ITY2|TABB)$'
                then 'year'
       end,
       case when period_code ~ '^\d{4}M\d{2}$'
                then cast(right(period_code, 2) as int)
            when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD|ITY1|ITY2|TABB)$'
                then cast(left(period_code, 4) as int)
       end,
       amount
FROM capital_upsert i
WHERE char_length(function_code) = 4 AND char_length(item_code) = 4;

COMMIT;
