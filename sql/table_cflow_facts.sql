-- Table: public.cflow_facts

-- DROP TABLE public.cflow_facts;

CREATE TABLE public.cflow_facts
(
  demarcation_code text,
  period_code text,
  item_code text,
  amount bigint,
  amount_type_code text,
  id serial,
  financial_year integer,
  period_length text,
  financial_period integer,
  CONSTRAINT cflow_facts_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.cflow_facts
  OWNER TO municipal_finance;
