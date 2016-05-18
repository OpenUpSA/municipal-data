-- Table: public.repmaint_facts

-- DROP TABLE public.repmaint_facts;

CREATE TABLE public.repmaint_facts
(
  demarcation_code text,
  period_code text,
  item_code text,
  amount bigint,
  id serial,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_code text,
  CONSTRAINT repmaint_facts_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.repmaint_facts
  OWNER TO municipal_finance;
