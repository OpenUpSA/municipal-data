
CREATE TABLE public.municipality_contacts
(
  demarcation_code text,
  postal_address_1 text,
  postal_address_2 text,
  postal_address_3 text,
  street_address_1 text,
  street_address_2 text,
  street_address_3 text,
  street_address_4 text,
  phone_number text,
  fax_number text,
  url text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.municipality_contacts
  OWNER TO municipal_finance;
