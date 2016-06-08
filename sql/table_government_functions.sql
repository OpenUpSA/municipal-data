-- DROP TABLE public.government_functions;

CREATE TABLE public.government_functions
(
  code text NOT NULL,
  label text,
  category_label text,
  subcategory_label text,
  CONSTRAINT government_functions_pkey PRIMARY KEY (code),
  CONSTRAINT government_functions_unique_code UNIQUE (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.government_functions
  OWNER TO municipal_finance;
