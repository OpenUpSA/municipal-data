-- Table: public.grants_labeled

-- DROP TABLE public.grants_labeled;

CREATE TABLE public.grants_labeled
(
  demacation_code text,
  period_code text,
  grant_code text,
  amount integer,
  grant_name text,
  amount_type_code text,
  id integer NOT NULL DEFAULT nextval('grants_labeled_id_seq'::regclass),
  demarcation_label text,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_label text,
  CONSTRAINT grants_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.grants_labeled
  OWNER TO municipal_finance;
