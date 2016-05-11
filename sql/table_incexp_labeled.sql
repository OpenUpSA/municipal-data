-- Table: public.incexp_labeled

-- DROP TABLE public.incexp_labeled;

CREATE TABLE public.incexp_labeled
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
  CONSTRAINT incexp_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.incexp_labeled
  OWNER TO municipal_finance;
