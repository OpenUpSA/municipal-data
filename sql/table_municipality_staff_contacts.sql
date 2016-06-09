-- Table: public.municipality_contacts

-- DROP TABLE public.municipality_staff_contacts;

CREATE TABLE public.municipality_staff_contacts
(
  demarcation_code text,
  role text,
  title text,
  name text,
  office_number text,
  fax_number text,
  email_address text,
  CONSTRAINT municipality_staff_contacts_pkey PRIMARY KEY (code),
  CONSTRAINT municipality_staff_contacts_unique_demarcation UNIQUE (demarcation_code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.municipality_staff_contacts
  OWNER TO municipal_finance;
