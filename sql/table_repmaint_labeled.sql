-- Table: public.repmaint_labeled

-- DROP TABLE public.repmaint_labeled;

CREATE TABLE public.repmaint_labeled
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
  CONSTRAINT repmaint_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.repmaint_labeled
  OWNER TO municipal_finance;
