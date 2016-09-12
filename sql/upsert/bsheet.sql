BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE bsheet_2016q4
(
        demarcation_code TEXT,
        period_code TEXT,
        item_code TEXT,
        amount DECIMAL
) ON COMMIT DROP;

\echo Read data...

\copy bsheet_2016q4 (demarcation_code, period_code, item_code, amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2016q4/Section 71 Q4 published data/bsheet_2016q4_acrmun.csv' DELIMITER ',' CSV HEADER;

\echo Drop not null constraints...

alter table bsheet_facts
      alter column financial_year drop not null,
      alter column amount_type_code drop not null,
      alter column period_length drop not null,
      alter column financial_period drop not null;

\echo Update changed values...

UPDATE bsheet_facts f
SET amount = i.amount
FROM bsheet_2016q4 i
WHERE f.demarcation_code = i.demarcation_code
AND f.period_code = i.period_code
AND f.item_code = i.item_code
AND f.amount != i.amount;

\echo Insert new values...

INSERT INTO bsheet_facts
(
    demarcation_code,
    period_code,
    item_code,
    amount
)
SELECT demarcation_code, period_code, item_code, amount
FROM bsheet_2016q4 i
WHERE
    NOT EXISTS (
        SELECT * FROM bsheet_facts f
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
    );

\echo Decode period_code...

update bsheet_facts set financial_year = cast(left(period_code, 4) as int) where financial_year is null;
update bsheet_facts set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD') and amount_type_code is null;
update bsheet_facts set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD') and amount_type_code is null;
update bsheet_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}' and period_length is null;
update bsheet_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}' and period_length is null;
update bsheet_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month' and financial_period is null;
update bsheet_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year' and financial_period is null;

\echo Add back not null constraints...

alter table bsheet_facts
      alter column financial_year set not null,
      alter column amount_type_code set not null,
      alter column period_length set not null,
      alter column financial_period set not null;

COMMIT;
