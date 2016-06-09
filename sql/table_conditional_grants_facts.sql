-- Table: public.conditional_grants_facts

-- DROP TABLE public.conditional_grants_facts;

CREATE TABLE public.conditional_grants_facts
(
  demarcation_code text,
  period_code text,
  grant_code text REFERENCES conditional_grants (code) MATCH FULL,
  amount bigint,
  amount_type_code text,
  id serial,
  financial_year integer,
  period_length text,
  financial_period integer,
  CONSTRAINT conditional_grants_facts_pkey PRIMARY KEY (id),
  CONSTRAINT conditional_grants_facts_unique_demarcation_period_item UNIQUE (demarcation_code, period_code, grant_code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.conditional_grants_facts
  OWNER TO municipal_finance;
