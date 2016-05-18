-- Table: public.bsheet_facts

-- DROP TABLE public.bsheet_facts;

CREATE TABLE public.bsheet_facts
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
  CONSTRAINT bsheet_facts_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.bsheet_facts
  OWNER TO municipal_finance;
