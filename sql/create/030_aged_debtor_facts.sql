-- Table: public.aged_debtor_facts

-- DROP TABLE public.aged_debtor_facts;

CREATE TABLE public.aged_debtor_facts
(
  demarcation_code text REFERENCES scorecard_geography (geo_code),
  period_code text,
  customer_group_code text,
  item_code text REFERENCES aged_debtor_items (code),
  bad_amount bigint,
  badi_amount bigint,
  g1_amount bigint,
  l1_amount bigint,
  l120_amount bigint,
  l150_amount bigint,
  l180_amount bigint,
  l30_amount bigint,
  l60_amount bigint,
  l90_amount bigint,
  total_amount bigint,
  id serial,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_code text,
  CONSTRAINT aged_debtor_facts_pkey PRIMARY KEY (id),
  CONSTRAINT aged_debtor_facts_unique_demarcation_period_item UNIQUE (demarcation_code, period_code, customer_group_code, item_code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.aged_debtor_facts
  OWNER TO municipal_finance;
