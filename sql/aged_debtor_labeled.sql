-- Table: public.aged_debtor_labeled

-- DROP TABLE public.aged_debtor_labeled;

CREATE TABLE public.aged_debtor_labeled
(
  demarcation_code text,
  period_code text,
  customer_grp_cde text,
  item_code text,
  bad_amount bigint,
  badi_amount bigint,
  g1_amount bigint,
  l1_amount bigint,
  l120_amount bigint,
  l150_amount bigint,
  l180_amount bigint,
  l30_amount bigint,
  l60_amount bigint,
  l90_amount bigint,
  total_amount bigint,
  item_label text,
  id integer NOT NULL DEFAULT nextval('aged_debtor_labeled_id_seq'::regclass),
  demarcation_label text,
  financial_year integer,
  period_length text,
  financial_period text,
  amount_type_code text,
  amount_type_label text,
  CONSTRAINT aged_debtor_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.aged_debtor_labeled
  OWNER TO municipal_finance;
