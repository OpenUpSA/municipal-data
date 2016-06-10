-- Table: public.amount_type

-- DROP TABLE public.amount_type;

CREATE TABLE public.amount_type
(
  code text NOT NULL,
  label text,
  id serial,
  CONSTRAINT amount_type_pkey PRIMARY KEY (id),
  CONSTRAINT amount_type_unique_code UNIQUE (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.amount_type
  OWNER TO municipal_finance;
