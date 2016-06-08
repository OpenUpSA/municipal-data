-- Table: public.capital_facts

-- DROP TABLE public.capital_facts;

CREATE TABLE public.capital_facts
(
  demarcation_code text,
  period_code text,
  function_code text,
  item_code text,
  new_assets bigint,
  renewal_of_existing bigint,
  total_assets bigint,
  repairs_maintenance bigint,
  asset_register_summary bigint,
  id serial,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_code text,
  CONSTRAINT capital_facts_pkey PRIMARY KEY (id),
  CONSTRAINT capital_facts_unique_demarcation_period_item UNIQUE (demarcation_code, period_code, item_code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.capital_facts
  OWNER TO municipal_finance;
