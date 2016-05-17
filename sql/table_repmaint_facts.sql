-- Table: public.repmaint_facts

-- DROP TABLE public.repmaint_facts;

CREATE TABLE public.repmaint_facts
(
  demarcation_code text,
  period_code text,
  item_code text,
  amount bigint,
  id serial,
  item_label text,
  demarcation_label text,
  financial_year text,
  period_length text,
  financial_period integer,
  amount_type_code text,
  amount_type_label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT repmaint_facts_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.repmaint_facts
  OWNER TO municipal_finance;
