-- Table: public.cflow_labeled

-- DROP TABLE public.cflow_labeled;

CREATE TABLE public.cflow_labeled
(
  demarcation_code text,
  period_code text,
  item_code text,
  amount bigint,
  amount_type_code text,
  item_label text,
  id integer NOT NULL DEFAULT nextval('cflow_labeled_id_seq'::regclass),
  demarcation_label text,
  financial_year integer,
  period_length text,
  financial_period integer,
  amount_type_label text,
  function_category text,
  CONSTRAINT cflow_labeled_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.cflow_labeled
  OWNER TO municipal_finance;
