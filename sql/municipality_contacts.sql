-- Table: public.municipality_contacts

-- DROP TABLE public.municipality_contacts;

CREATE TABLE public.municipality_contacts
(
  demarcation_code text,
  role text,
  title text,
  name text,
  office_number text,
  fax_number text,
  email_address text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.municipality_contacts
  OWNER TO municipal_finance;
