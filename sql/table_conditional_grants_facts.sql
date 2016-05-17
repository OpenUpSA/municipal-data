-- Table: public.conditional_grants_facts

-- DROP TABLE public.conditional_grants_facts;

CREATE TABLE public.conditional_grants_facts
(
  demacation_code text,
  period_code text,
  grant_code text,
  amount bigint,
  amount_type_code text,
  id serial,
  financial_year integer,
  period_length text,
  financial_period integer,
  CONSTRAINT conditional_grants_facts_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.conditional_grants_facts
  OWNER TO municipal_finance;
