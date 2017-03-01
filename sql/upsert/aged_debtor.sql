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

\copy aged_debtor_upsert (demarcation_code, period_code, customer_group_code, item_code, bad_amount, badi_amount, g1_amount, l1_amount, l120_amount, l150_amount, l180_amount, l30_amount, l60_amount, l90_amount, total_amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2017q1/debt_2017q1_acrmun.csv' DELIMITER ',' CSV HEADER;

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
    total_amount,
    financial_year,
    amount_type_code,
    period_length,
    financial_period
)
SELECT demarcation_code,
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
       total_amount,
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
FROM aged_debtor_upsert i
WHERE i.item_code NOT IN (' Inc', ' Ren');

COMMIT;
