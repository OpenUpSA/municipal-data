BEGIN;

CREATE TEMPORARY TABLE bsheet_2016q3
(
        demarcation_code TEXT,
        period_code TEXT,
        item_code TEXT,
        amount text
) ON COMMIT DROP;

\copy bsheet_2016q3 (demarcation_code, period_code, item_code, amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2016q3/bsheet_2016q3_acrmun.csv' DELIMITER ',' CSV HEADER;

UPDATE bsheet_facts f
SET amount = round(i.amount::float)
FROM bsheet_2016q3 i
WHERE f.demarcation_code = i.demarcation_code
AND f.period_code = i.period_code
AND f.amount != round(i.amount::float);

INSERT INTO bsheet_facts
(
    demarcation_code,
    period_code,
    item_code,
    amount
)
SELECT demarcation_code, period_code, item_code, round(amount::float)
FROM bsheet_2016q3 i
WHERE
    NOT EXISTS (
        SELECT * FROM bsheet_facts f
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
    );

\echo 'bsheet'
update bsheet_facts set financial_year = cast(left(period_code, 4) as int);
update bsheet_facts set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update bsheet_facts set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update bsheet_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update bsheet_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update bsheet_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update bsheet_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';

COMMIT;
