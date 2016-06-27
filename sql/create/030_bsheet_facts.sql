-- Table: public.bsheet_facts

-- DROP TABLE public.bsheet_facts;

CREATE TABLE public.bsheet_facts
(
  demarcation_code TEXT NOT NULL REFERENCES scorecard_geography (geo_code),
  period_code TEXT NOT NULL,
  item_code TEXT REFERENCES bsheet_items (code),
  amount bigint,
  id serial,
  financial_year INTEGER NOT NULL,
  period_length TEXT NOT NULL,
  financial_period INTEGER NOT NULL ,
  amount_type_code TEXT NOT NULL,
  CONSTRAINT bsheet_facts_pkey PRIMARY KEY (id),
  CONSTRAINT bsheet_facts_unique_demarcation_period_item UNIQUE (demarcation_code, period_code, item_code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.bsheet_facts
  OWNER TO municipal_finance;
