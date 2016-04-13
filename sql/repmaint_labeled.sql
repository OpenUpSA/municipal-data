-- Table: public.repmaint_labeled

-- DROP TABLE public.repmaint_labeled;

CREATE TABLE public.repmaint_labeled
(
  demarcation_code text,
  period_code text,
  item_code text,
  act_or_bud_amt bigint,
  id integer NOT NULL DEFAULT nextval('repmaint_labeled_id_seq'::regclass),
  item_label text,
  demarcation_desc text,
  financial_year text,
  period_length text,
  financial_period text,
  amount_type_cde text,
  amount_type_desc text,
  CONSTRAINT repmaint_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.repmaint_labeled
  OWNER TO municipal_finance;
