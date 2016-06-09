-- Table: public.bsheet_facts

-- DROP TABLE public.bsheet_facts;

CREATE TABLE public.bsheet_facts
(
  demarcation_code text REFERENCES scorecard_geography (geo_code),
  period_code text,
  item_code text,
  amount bigint,
  id serial,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_code text,
  CONSTRAINT bsheet_facts_pkey PRIMARY KEY (id),
  CONSTRAINT bsheet_facts_unique_demarcation_period_item UNIQUE (demarcation_code, period_code, item_code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.bsheet_facts
  OWNER TO municipal_finance;
