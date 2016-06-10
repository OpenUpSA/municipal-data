-- Table: public.incexp_facts

-- DROP TABLE public.incexp_facts;

CREATE TABLE public.incexp_facts
(
  demarcation_code text REFERENCES scorecard_geography (geo_code),
  period_code text,
  function_code text REFERENCES incexp_items (code) MATCH FULL,
  item_code text REFERENCES incexp_items (code) MATCH FULL,
  amount bigint,
  id serial,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_code text,
  CONSTRAINT incexp_facts_pkey PRIMARY KEY (id),
  CONSTRAINT incexp_facts_unique_demarcation_period_function_item UNIQUE (demarcation_code, period_code, function_code, item_code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.incexp_facts
  OWNER TO municipal_finance;
