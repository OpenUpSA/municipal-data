-- Table: public.grants_facts

-- DROP TABLE public.grants_facts;

CREATE TABLE public.grants_facts
(
  demacation_code text,
  period_code text,
  grant_code text,
  amount integer,
  grant_name text,
  amount_type_code text,
  id serial,
  demarcation_label text,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_label text,
  CONSTRAINT grants_facts_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.grants_facts
  OWNER TO municipal_finance;
