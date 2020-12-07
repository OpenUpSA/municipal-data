BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE grant_upsert
(
        demarcation_code TEXT,
        period_code TEXT,
        grant_code TEXT,
        amount DECIMAL
) ON COMMIT DROP;

\echo Read data...

\copy grant_upsert (demarcation_code, period_code, grant_code, amount) FROM '' DELIMITER ',' CSV HEADER;

\echo Delete demarcation_code-period_code pairs that are in the update

DELETE FROM grant_facts_v2 f WHERE EXISTS (
        SELECT 1 FROM grant_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        LIMIT 1
    );

\echo Insert new values...

INSERT INTO grant_facts_v2
(
    demarcation_code,
    period_code,
    grant_type_id,
    amount_type_id,
    amount,
    financial_year,
    period_length,
    financial_period
)
SELECT demarcation_code,
       period_code,
       (select id from grant_types_v2 where grant_types_v2.code = grant_code),
       case when period_code ~ '^\d{4}(ADJB|ORGB|SCHD|TRFR)(M\d{2})?$'
               then (select id from amount_type_v2 where amount_type_v2.code = substr(period_code, 5, 4))
           when period_code ~ '^\d{4}M\d{2}$'
               then (select id from amount_type_v2 where amount_type_v2.code = 'ACT')
       end,
       amount,
       cast(left(period_code, 4) as int),
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
FROM grant_upsert i;

COMMIT;
