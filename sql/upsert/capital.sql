BEGIN;

CREATE TEMPORARY TABLE capital_import (
    demarcation_code TEXT,
    period_code TEXT,
    item_code TEXT,
    function_code TEXT,
    new_assets BIGINT,
    renewal_of_existing FLOAT,
    total_assets BIGINT,
    repairs_maintenance FLOAT,
    asset_register_summary BIGINT,
    financial_year INTEGER,
    amount_type_code TEXT,
    period_length TEXT,
    financial_period INTEGER
) ON COMMIT DROP;

\copy capital_import (demarcation_code, period_code, function_code, item_code, new_assets, renewal_of_existing, total_assets, repairs_maintenance, asset_register_summary) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2016q3/capital_2016q3_acrmun.csv' DELIMITER ',' CSV HEADER;

-- 2016Q3 Delete the following function codes that were entered incorrectly as confirmed with Treasury 2016-06-28
delete from capital_import where function_code in ('AC','BT','CL','CM','ER','HA','HO','HR','HS','IL','IT','LB','LT','MC','MM','OA','OS','PF','PK','PL','PT','PY','RD','RO','RR','SL','SR','TR','WD','WP');

update capital_import set financial_year = cast(left(period_code, 4) as int);
update capital_import set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update capital_import set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update capital_import set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update capital_import set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update capital_import set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update capital_import set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';

UPDATE capital_facts f
SET demarcation_code = i.demarcation_code,
    period_code = i.period_code,
    item_code = i.item_code,
    function_code = i.function_code,
    new_assets = i.new_assets,
    renewal_of_existing = round(i.renewal_of_existing),
    total_assets = i.renewal_of_existing,
    repairs_maintenance = round(i.repairs_maintenance),
    asset_register_summary = i.asset_register_summary,
    financial_year = i.financial_year,
    amount_type_code = i.amount_type_code,
    period_length = i.period_length,
    financial_period = i.financial_period
FROM capital_import i
WHERE f.demarcation_code = i.demarcation_code
AND f.period_code = i.period_code
AND f.item_code = i.item_code
AND f.function_code = i.function_code
AND (f.new_assets != i.new_assets
  OR f.renewal_of_existing != round(i.renewal_of_existing)
  OR f.total_assets != i.total_assets
  OR f.repairs_maintenance != round(i.repairs_maintenance)
  OR f.asset_register_summary != i.asset_register_summary);

INSERT INTO capital_facts
(
    demarcation_code,
    period_code,
    item_code,
    function_code,
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
       item_code,
       function_code,
       new_assets,
       round(renewal_of_existing),
       total_assets,
       round(repairs_maintenance),
       asset_register_summary,
       financial_year,
       amount_type_code,
       period_length,
       financial_period
FROM capital_import i
WHERE
    NOT EXISTS (
        SELECT 1 FROM capital_facts f
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        AND f.item_code = i.item_code
        AND f.function_code = i.function_code
    );

COMMIT;
