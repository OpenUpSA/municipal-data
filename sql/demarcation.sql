-- Table: public.demarcation

-- DROP TABLE public.demarcation;

CREATE TABLE public.demarcation
(
  name text,
  code text NOT NULL,
  CONSTRAINT demarcation_pkey PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.demarcation
  OWNER TO postgres;
