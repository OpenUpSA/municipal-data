BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE conditional_grants_upsert
(
        demarcation_code TEXT,
        period_code TEXT,
        grant_code TEXT,
        amount DECIMAL
) ON COMMIT DROP;

\echo Read data...

\copy conditional_grants_upsert (demarcation_code, period_code, grant_code, amount) FROM '/home/jdb/proj/code4sa/municipalmoney/data/Section 71 Q3 2018-19/grants_2019q3_acrmun.csv' DELIMITER ',' CSV HEADER;

\echo Delete demarcation_code-period_code pairs that are in the update

DELETE FROM conditional_grants_facts f WHERE EXISTS (
        SELECT 1 FROM conditional_grants_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        LIMIT 1
    );

\echo Insert new values...

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
       amount,
       cast(left(period_code, 4) as int),
       case when period_code ~ '^\d{4}(ADJB|ORGB|SCHD|TRFR)(M\d{2})?$'
               then substr(period_code, 5, 4)
           when period_code ~ '^\d{4}M\d{2}$'
               then 'ACT'
       end,
       case when period_code ~ '^\d{4}M\d{2}$'
                then 'month'
            when period_code ~ '^\d{4}(ADJB|ORGB|SCHD|TRFR)$'
                then 'year'
       end,
       case when period_code ~ '^\d{4}M\d{2}$'
                then cast(right(period_code, 2) as int)
            when period_code ~ '^\d{4}(ADJB|ORGB|SCHD|TRFR)$'
                then cast(left(period_code, 4) as int)
       end
FROM conditional_grants_upsert i;

COMMIT;
