BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE aged_debtor_upsert
(
        demarcation_code TEXT,
        period_code TEXT,
        customer_group_code TEXT,
        item_code TEXT,
        bad_amount DECIMAL,
        badi_amount DECIMAL,
        g1_amount DECIMAL,
        l1_amount DECIMAL,
        l120_amount DECIMAL,
        l150_amount DECIMAL,
        l180_amount DECIMAL,
        l30_amount DECIMAL,
        l60_amount DECIMAL,
        l90_amount DECIMAL,
        total_amount DECIMAL
) ON COMMIT DROP;

\echo Read data...

\copy aged_debtor_upsert (demarcation_code, period_code, customer_group_code, item_code, bad_amount, badi_amount, g1_amount, l1_amount, l120_amount, l150_amount, l180_amount, l30_amount, l60_amount, l90_amount, total_amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2016q4/debt_2016q4_acrmun.csv' DELIMITER ',' CSV HEADER;

\echo Drop not null constraints...

alter table aged_debtor_facts
      alter column financial_year drop not null,
      alter column amount_type_code drop not null,
      alter column period_length drop not null,
      alter column financial_period drop not null;

\echo Delete demarcation_code-period_code pairs that are in the update

DELETE FROM aged_debtor_facts f WHERE EXISTS (
        SELECT 1 FROM aged_debtor_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        LIMIT 1
    );

\echo Insert new values...

INSERT INTO aged_debtor_facts
(
    demarcation_code,
    period_code,
    customer_group_code,
    item_code,
    bad_amount,
    badi_amount,
    g1_amount,
    l1_amount,
    l120_amount,
    l150_amount,
    l180_amount,
    l30_amount,
    l60_amount,
    l90_amount,
    total_amount
)
SELECT demarcation_code, period_code, customer_group_code, item_code, bad_amount, badi_amount, g1_amount, l1_amount, l120_amount, l150_amount, l180_amount, l30_amount, l60_amount, l90_amount, total_amount
FROM aged_debtor_upsert i
WHERE i.item_code NOT IN (' Inc', ' Ren');

\echo Decode period_code...

update aged_debtor_facts set financial_year = cast(left(period_code, 4) as int) where financial_year is null;
update aged_debtor_facts set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD') and amount_type_code is null;
update aged_debtor_facts set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD') and amount_type_code is null;
update aged_debtor_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}' and period_length is null;
update aged_debtor_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}' and period_length is null;
update aged_debtor_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month' and financial_period is null;
update aged_debtor_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year' and financial_period is null;

\echo Add back not null constraints...

alter table aged_debtor_facts
      alter column financial_year set not null,
      alter column amount_type_code set not null,
      alter column period_length set not null,
      alter column financial_period set not null;

COMMIT;
