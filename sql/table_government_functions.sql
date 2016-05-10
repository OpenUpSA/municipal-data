-- DROP TABLE public.government_functions;

CREATE TABLE public.government_functions
(
  code text NOT NULL,
  label text,
  CONSTRAINT government_functions_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.government_functions
  OWNER TO municipal_finance;
