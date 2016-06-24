-- Table: public.cflow_facts

-- DROP TABLE public.cflow_facts;

CREATE TABLE public.cflow_facts
(
  demarcation_code text REFERENCES scorecard_geography (geo_code),
  period_code text,
  item_code text REFERENCES cflow_items (code),
  amount bigint,
  amount_type_code text,
  id serial,
  financial_year integer,
  period_length text,
  financial_period integer,
  CONSTRAINT cflow_facts_pkey PRIMARY KEY (id),
  CONSTRAINT cflow_facts_unique_demarcation_period_item UNIQUE (demarcation_code, period_code, item_code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.cflow_facts
  OWNER TO municipal_finance;
