-- drop table bsheet_labels;
-- drop table aged_creditors_labels;
-- drop table aged_debtors_labels;
-- drop table capital_labels;
-- drop table cflow_labels;
-- drop table incexp_labels;
-- drop table repmaint_labels;

CREATE TABLE public.bsheet_labels
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT bsheet_labels_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.bsheet_labels
  OWNER TO municipal_finance;



CREATE TABLE public.aged_creditors_labels
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT aged_creditors_labels_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.aged_creditors_labels
  OWNER TO municipal_finance;



CREATE TABLE public.aged_debtors_labels
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT aged_debtors_labels_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.aged_debtors_labels
  OWNER TO municipal_finance;



CREATE TABLE public.capital_labels
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT capital_labels_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.capital_labels
  OWNER TO municipal_finance;



CREATE TABLE public.cflow_labels
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT cflow_labels_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.cflow_labels
  OWNER TO municipal_finance;


CREATE TABLE public.incexp_labels
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT incexp_labels_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.incexp_labels
  OWNER TO municipal_finance;



CREATE TABLE public.repmaint_labels
(
  code text NOT NULL,
  label text,
  position_in_return_form integer,
  return_form_structure text,
  composition text,
  CONSTRAINT repmaint_labels_primary_key PRIMARY KEY (code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.repmaint_labels
  OWNER TO municipal_finance;
