BEGIN;

CREATE TEMPORARY TABLE bsheet_import (
    demarcation_code TEXT,
    period_code TEXT,
    item_code TEXT,
    amount FLOAT,
    financial_year INTEGER,
    amount_type_code TEXT,
    period_length TEXT,
    financial_period INTEGER
) ON COMMIT DROP;

\copy bsheet_import (demarcation_code, period_code, item_code, amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2016q3/bsheet_2016q3_acrmun.csv' DELIMITER ',' CSV HEADER;

UPDATE bsheet_import SET financial_year = cast(left(period_code, 4) AS int);
UPDATE bsheet_import SET amount_type_code = substr(period_code, 5) WHERE substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
UPDATE bsheet_import SET amount_type_code = 'ACT' WHERE substr(period_code, 5) NOT in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
UPDATE bsheet_import SET period_length = 'year' WHERE substr(period_code, 5, 3) NOT SIMILAR to 'M\d{2}';
UPDATE bsheet_import SET period_length = 'month' WHERE substr(period_code, 5, 3) SIMILAR to 'M\d{2}';
UPDATE bsheet_import SET financial_period = cast(right(period_code, 2) AS int) WHERE period_length = 'month';
UPDATE bsheet_import SET financial_period = cast(left(period_code, 4) AS int) WHERE period_length = 'year';

UPDATE bsheet_facts f
SET demarcation_code = i.demarcation_code,
    period_code = i.period_code,
    item_code = i.item_code,
    amount = round(i.amount),
    financial_year = i.financial_year,
    amount_type_code = i.amount_type_code,
    period_length = i.period_length,
    financial_period = i.financial_period
FROM bsheet_import i
WHERE f.demarcation_code = i.demarcation_code
AND f.period_code = i.period_code
AND f.item_code = i.item_code
AND f.amount != round(i.amount);

INSERT INTO bsheet_facts
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
FROM bsheet_import i
WHERE
    NOT EXISTS (
        SELECT 1 FROM bsheet_facts f
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        AND f.item_code = i.item_code
    );

COMMIT;
