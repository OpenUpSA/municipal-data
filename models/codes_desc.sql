-- Table: public.codes_desc

-- DROP TABLE public.codes_desc;

CREATE TABLE public.codes_desc
(
  column_name text NOT NULL,
  code text NOT NULL,
  description text,
  CONSTRAINT codes_desc_primary_key PRIMARY KEY (column_name, code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.codes_desc
  OWNER TO postgres;
