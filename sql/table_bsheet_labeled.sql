-- Table: public.bsheet_labeled

-- DROP TABLE public.bsheet_labeled;

CREATE TABLE public.bsheet_labeled
(
  demarcation_code text,
  period_code text,
  item_code text,
  amount bigint,
  item_label text,
  id serial,
  demarcation_label text,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_code text,
  amount_type_label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT bsheet_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.bsheet_labeled
  OWNER TO municipal_finance;
