BEGIN;

CREATE TEMPORARY TABLE repmaint_import (
    demarcation_code TEXT,
    period_code TEXT,
    item_code TEXT,
    amount FLOAT,
    financial_year INTEGER,
    amount_type_code TEXT,
    period_length TEXT,
    financial_period INTEGER
) ON COMMIT DROP;

\copy repmaint_import (demarcation_code, period_code, item_code, amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2016q3/rm_2016q3_acrmun.csv' DELIMITER ',' CSV HEADER;

update repmaint_import set financial_year = cast(left(period_code, 4) as int);
update repmaint_import set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update repmaint_import set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update repmaint_import set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update repmaint_import set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update repmaint_import set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update repmaint_import set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';

UPDATE repmaint_facts f
SET demarcation_code = i.demarcation_code,
    period_code = i.period_code,
    item_code = i.item_code,
    amount = round(i.amount),
    financial_year = i.financial_year,
    amount_type_code = i.amount_type_code,
    period_length = i.period_length,
    financial_period = i.financial_period
FROM repmaint_import i
WHERE f.demarcation_code = i.demarcation_code
AND f.period_code = i.period_code
AND f.item_code = i.item_code
AND f.amount != round(i.amount);

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
       round(amount),
       financial_year,
       amount_type_code,
       period_length,
       financial_period
FROM repmaint_import i
WHERE
    NOT EXISTS (
        SELECT 1 FROM repmaint_facts f
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        AND f.item_code = i.item_code
    );

COMMIT;
