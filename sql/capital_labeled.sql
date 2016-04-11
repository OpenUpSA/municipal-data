-- Table: public.capital_labeled

-- DROP TABLE public.capital_labeled;

CREATE TABLE public.capital_labeled
(
  demarcation_code text,
  period_code text,
  function_cde text,
  capital_cde text,
  new_assets bigint,
  renewal_of_existing bigint,
  total_assets bigint,
  repairs_maintenance bigint,
  asset_register_summary bigint,
  function_desc text,
  capital_desc text,
  id serial,
  demarcation_desc text,
  financial_year text,
  period_length text,
  financial_period text,
  amount_type_cde text,
  amount_type_desc text,
  CONSTRAINT capital_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.capital_labeled
  OWNER TO municipal_finance;
