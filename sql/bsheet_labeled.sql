-- Table: public.bsheet_labeled

-- DROP TABLE public.bsheet_labeled;

CREATE TABLE public.bsheet_labeled
(
  demarcation_code text,
  period_code text,
  item_code text,
  amount bigint,
  item_label text,
  id integer NOT NULL DEFAULT nextval('bsheet_labeled_id_seq'::regclass),
  demarcation_label text,
  financial_year integer,
  period_length text,
  financial_period text,
  amount_type_code text,
  amount_type_label text,
  CONSTRAINT bsheet_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.bsheet_labeled
  OWNER TO municipal_finance;
