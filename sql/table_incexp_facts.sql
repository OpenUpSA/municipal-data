-- Table: public.incexp_facts

-- DROP TABLE public.incexp_facts;

CREATE TABLE public.incexp_facts
(
  demarcation_code text,
  period_code text,
  function_code text,
  item_code text,
  amount bigint,
  id serial,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_code text,
  CONSTRAINT incexp_facts_pkey PRIMARY KEY (id),
  CONSTRAINT incexp_facts_unique_demarcation_period_item UNIQUE (demarcation_code, period_code, item_code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.incexp_facts
  OWNER TO municipal_finance;
