-- Table: public.aged_creditor_labeled

-- DROP TABLE public.aged_creditor_labeled;

CREATE TABLE public.aged_creditor_labeled
(
  demarcation_code text,
  period_code text,
  age_cde text,
  g1_amount bigint,
  l1_amount bigint,
  l120_amount bigint,
  l150_amount bigint,
  l180_amount bigint,
  l30_amount bigint,
  l60_amount bigint,
  l90_amount bigint,
  total_amount bigint,
  aged_creditor_desc text,
  id serial,
  demarcation_desc text,
  financial_year text,
  period_length text,
  financial_period text,
  amount_type_cde text,
  amount_type_desc text,
  CONSTRAINT aged_creditor_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.aged_creditor_labeled
  OWNER TO municipal_finance;
