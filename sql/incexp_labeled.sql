-- Table: public.incexp_labeled

-- DROP TABLE public.incexp_labeled;

CREATE TABLE public.incexp_labeled
(
  demarcation_code text,
  period_code text,
  function_cde text,
  function_desc text,
  incexp_cde text,
  incexp_desc text,
  act_or_bud_amt bigint,
  id integer NOT NULL DEFAULT nextval('incexp_labeled_id_seq'::regclass),
  demarcation_desc text,
  financial_year text,
  period_length text,
  financial_period text,
  amount_type_cde text,
  amount_type_desc text,
  CONSTRAINT incexp_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.incexp_labeled
  OWNER TO municipal_finance;
