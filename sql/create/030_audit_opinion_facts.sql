-- Table: public.audit_opinion_facts

-- DROP TABLE public.audit_report_import;
-- DROP TABLE public.audit_opinion_facts;

CREATE TABLE public.audit_report_import
(
  demarcation_code text NOT NULL REFERENCES scorecard_geography (geo_code),
  financial_year integer NOT NULL,
  report_url text,
  CONSTRAINT audit_report_import_composit_pkey UNIQUE (demarcation_code, financial_year)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.audit_report_import
  OWNER TO municipal_finance;

CREATE TABLE public.audit_opinion_facts
(
  demarcation_code text NOT NULL REFERENCES scorecard_geography (geo_code),
  financial_year integer NOT NULL,
  opinion_code text NOT NULL,
  opinion_label text NOT NULL,
  report_url text,
  id serial,
  CONSTRAINT audit_opinion_facts_pkey PRIMARY KEY (id),
  CONSTRAINT audit_opinion_facts_unique_demarcation_financial_year UNIQUE (demarcation_code, financial_year)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.audit_opinion_facts
  OWNER TO municipal_finance;
