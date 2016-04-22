drop table bsheet_labels;
drop table aged_creditors_labels;
drop table aged_debtors_labels;
drop table capital_labels;
drop table cflow_labels;
drop table incexp_labels;
drop table repmaint_labels;

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



alter table aged_creditor_labeled add column position_in_return_form integer;
alter table aged_creditor_labeled add column return_form_structure text;
alter table aged_creditor_labeled add column composition text;

alter table aged_debtor_labeled add column position_in_return_form integer;
alter table aged_debtor_labeled add column return_form_structure text;
alter table aged_debtor_labeled add column composition text;

alter table capital_labeled add column position_in_return_form integer;
alter table capital_labeled add column return_form_structure text;
alter table capital_labeled add column composition text;

alter table bsheet_labeled add column position_in_return_form integer;
alter table bsheet_labeled add column return_form_structure text;
alter table bsheet_labeled add column composition text;

alter table cflow_labeled add column position_in_return_form integer;
alter table cflow_labeled add column return_form_structure text;
alter table cflow_labeled add column composition text;

alter table incexp_labeled add column position_in_return_form integer;
alter table incexp_labeled add column return_form_structure text;
alter table incexp_labeled add column composition text;

alter table repmaint_labeled add column position_in_return_form integer;
alter table repmaint_labeled add column return_form_structure text;
alter table repmaint_labeled add column composition text;

update bsheet_labeled set position_in_return_form = subquery.position_in_return_form, return_form_structure = subquery.return_form_structure, composition = subquery.composition from (select * from bsheet_labels ) as subquery where subquery.code = item_code

update aged_creditor_labeled set position_in_return_form = subquery.position_in_return_form, return_form_structure = subquery.return_form_structure, composition = subquery.composition from (select * from aged_creditors_labels ) as subquery where subquery.code = item_code;
update aged_creditor_labeled set position_in_return_form = subquery.position_in_return_form, return_form_structure = subquery.return_form_structure, composition = subquery.composition from (select * from aged_debtors_labels ) as subquery where subquery.code = item_code;
update capital_labeled set position_in_return_form = subquery.position_in_return_form, return_form_structure = subquery.return_form_structure, composition = subquery.composition from (select * from capital_labels ) as subquery where subquery.code = item_code;
update cflow_labeled set position_in_return_form = subquery.position_in_return_form, return_form_structure = subquery.return_form_structure, composition = subquery.composition from (select * from cflow_labels ) as subquery where subquery.code = item_code;
update incexp_labeled set position_in_return_form = subquery.position_in_return_form, return_form_structure = subquery.return_form_structure, composition = subquery.composition from (select * from incexp_labels ) as subquery where subquery.code = item_code;
update repmaint_labeled set position_in_return_form = subquery.position_in_return_form, return_form_structure = subquery.return_form_structure, composition = subquery.composition from (select * from repmaint_labels ) as subquery where subquery.code = item_code;
