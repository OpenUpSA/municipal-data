-- DROP TABLE bsheet_items;
-- DROP TABLE aged_creditor_items;
-- DROP TABLE aged_debtor_items;
-- DROP TABLE capital_items;
-- DROP TABLE cflow_items;
-- DROP TABLE incexp_items;
-- DROP TABLE repmaint_items;

CREATE TABLE public.bsheet_items
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT bsheet_items_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.bsheet_items
  OWNER TO municipal_finance;



CREATE TABLE public.aged_creditor_items
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT aged_creditor_items_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.aged_creditor_items
  OWNER TO municipal_finance;



CREATE TABLE public.aged_debtor_items
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT aged_debtor_items_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.aged_debtor_items
  OWNER TO municipal_finance;



CREATE TABLE public.capital_items
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT capital_items_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.capital_items
  OWNER TO municipal_finance;



CREATE TABLE public.cflow_items
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT cflow_items_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.cflow_items
  OWNER TO municipal_finance;


CREATE TABLE public.incexp_items
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT incexp_items_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.incexp_items
  OWNER TO municipal_finance;



CREATE TABLE public.repmaint_items
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT repmaint_items_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.repmaint_items
  OWNER TO municipal_finance;


CREATE TABLE public.conditional_grants
(
  code text,
  name text,
  id serial,
  CONSTRAINT conditional_grants_pkey PRIMARY KEY (id),
  CONSTRAINT conditional_grants_unique_code UNIQUE (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.conditional_grants
  OWNER TO municipal_finance;
