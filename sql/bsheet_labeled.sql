-- Table: public.bsheet_labeled

-- DROP TABLE public.bsheet_labeled;

CREATE TABLE public.bsheet_labeled
(
  demarcation_code text,
  period_code text,
  bsheet_cde text,
  act_or_bud_amt bigint,
  bsheet_desc text,
  id serial,
  demarcation_desc text,
  financial_year text,
  period_length text,
  financial_period text,
  amount_type_cde text,
  amount_type_desc text,
  CONSTRAINT bsheet_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.bsheet_labeled
  OWNER TO municipal_finance;
