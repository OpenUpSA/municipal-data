BEGIN;

CREATE TEMPORARY TABLE conditional_grants_import (
    demarcation_code TEXT,
    period_code TEXT,
    grant_code TEXT,
    amount FLOAT,
    financial_year INTEGER,
    amount_type_code TEXT,
    period_length TEXT,
    financial_period INTEGER
) ON COMMIT DROP;

\copy conditional_grants_import (demarcation_code, period_code, grant_code, amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2016q3/grants_2016q3_acrmun.csv' DELIMITER ',' CSV HEADER;

update conditional_grants_import set financial_year = cast(left(period_code, 4) as int);
update conditional_grants_import set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD', 'TRFR', 'SCHD');
update conditional_grants_import set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD', 'TRFR', 'SCHD');
update conditional_grants_import set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update conditional_grants_import set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update conditional_grants_import set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update conditional_grants_import set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';

UPDATE conditional_grants_facts f
SET demarcation_code = i.demarcation_code,
    period_code = i.period_code,
    grant_code = i.grant_code,
    amount = round(i.amount),
    financial_year = i.financial_year,
    amount_type_code = i.amount_type_code,
    period_length = i.period_length,
    financial_period = i.financial_period
FROM conditional_grants_import i
WHERE f.demarcation_code = i.demarcation_code
AND f.period_code = i.period_code
AND f.grant_code = i.grant_code
AND f.amount != round(i.amount);

INSERT INTO conditional_grants_facts
(
    demarcation_code,
    period_code,
    grant_code,
    amount,
    financial_year,
    amount_type_code,
    period_length,
    financial_period
)
SELECT demarcation_code,
       period_code,
       grant_code,
       round(amount),
       financial_year,
       amount_type_code,
       period_length,
       financial_period
FROM conditional_grants_import i
WHERE
    NOT EXISTS (
        SELECT 1 FROM conditional_grants_facts f
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        AND f.grant_code = i.grant_code
    );

COMMIT;
