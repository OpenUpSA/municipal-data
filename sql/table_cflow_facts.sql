-- Table: public.cflow_facts

-- DROP TABLE public.cflow_facts;

CREATE TABLE public.cflow_facts
(
  demarcation_code text,
  period_code text,
  item_code text,
  amount bigint,
  amount_type_code text,
  item_label text,
  id serial,
  demarcation_label text,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_label text,
  function_category text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT cflow_facts_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.cflow_facts
  OWNER TO municipal_finance;
