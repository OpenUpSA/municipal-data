-- Table: public.incexp_facts

-- DROP TABLE public.incexp_facts;

CREATE TABLE public.incexp_facts
(
  demarcation_code text,
  period_code text,
  function_code text,
  item_code text,
  amount bigint,
  function_label text,
  item_label text,
  id serial,
  demarcation_label text,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_code text,
  amount_type_label text,
  function_category text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT incexp_facts_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.incexp_facts
  OWNER TO municipal_finance;
