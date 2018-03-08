\set ON_ERROR_STOP on

BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE capital_upsert
(
        demarcation_code TEXT,
        period_code TEXT,
        function_code TEXT,
        item_code TEXT,
        new_assets DECIMAL,
        renewal_of_existing DECIMAL,
        total_assets DECIMAL,
        repairs_maintenance DECIMAL,
        asset_register_summary DECIMAL
) ON COMMIT DROP;
CREATE INDEX capital_upsert_demarcation_code on capital_upsert (demarcation_code);
CREATE INDEX capital_upsert_period_code on capital_upsert (period_code);

\echo Read data...

\copy capital_upsert (demarcation_code, period_code, function_code, item_code, new_assets, renewal_of_existing, total_assets, repairs_maintenance, asset_register_summary) FROM '/home/jdb/proj/code4sa/municipalmoney/data/Section 71 Q1 2017-18/capital_2018q1_acrmun-KZN275-invalid-submissions-removed.csv' DELIMITER ',' CSV HEADER;

\echo Delete demarcation_code-period_code pairs that are in the update

DELETE FROM capital_facts f WHERE EXISTS (
        SELECT 1 FROM capital_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        LIMIT 1
    );

\echo Insert new values...

INSERT INTO capital_facts
(
    demarcation_code,
    period_code,
    function_code,
    item_code,
    new_assets,
    renewal_of_existing,
    total_assets,
    repairs_maintenance,
    asset_register_summary,
    financial_year,
    amount_type_code,
    period_length,
    financial_period
)
SELECT demarcation_code,
       period_code,
       function_code,
       item_code,
       new_assets,
       renewal_of_existing,
       total_assets,
       repairs_maintenance,
       asset_register_summary,
       cast(left(period_code, 4) as int),
       case when substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD')
               then substr(period_code, 5)
           when period_code ~ '^\d{4}M\d{2}$'
               then 'ACT'
       end,
       case when period_code ~ '^\d{4}M\d{2}$'
                then 'month'
            when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD)$'
                then 'year'
       end,
       case when period_code ~ '^\d{4}M\d{2}$'
                then cast(right(period_code, 2) as int)
            when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD)$'
                then cast(left(period_code, 4) as int)
       end
FROM capital_upsert i
WHERE char_length(function_code) = 4 AND char_length(item_code) = 4;

COMMIT;
