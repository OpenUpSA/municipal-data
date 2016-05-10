-- Table: public.amount_type

-- DROP TABLE public.amount_type;

CREATE TABLE public.amount_type
(
  code text NOT NULL,
  name text,
  CONSTRAINT amount_type_pkey PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.amount_type
  OWNER TO postgres;
