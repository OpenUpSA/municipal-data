CREATE TABLE public.badexp_facts
(
  demarcation_code text,
  financial_year integer,
  item_code text,
  item_label text,
  amount bigint,
  id serial,
  CONSTRAINT badexp_facts_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.badexp_facts
  OWNER TO municipal_finance;
