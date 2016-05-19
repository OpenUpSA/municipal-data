-- Table: public.audit_opinion_facts

-- DROP TABLE public.audit_opinion_facts;

CREATE TABLE public.audit_opinion_facts
(
  demarcation_code text NOT NULL,
  financial_year text NOT NULL,
  opinion_code text NOT NULL,
  opinion_label text NOT NULL,
  CONSTRAINT audit_opinion_facts_demarcation_code_financial_year_key UNIQUE (demarcation_code, financial_year)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.audit_opinion_facts
  OWNER TO municipal_finance;

-- Index: public.audit_opinion_facts_demarcation_code_idx

-- DROP INDEX public.audit_opinion_facts_demarcation_code_idx;

CREATE INDEX audit_opinion_facts_demarcation_code_idx
  ON public.audit_opinion_facts
  USING btree
  (demarcation_code COLLATE pg_catalog."default");

-- Index: public.audit_opinion_facts_financial_year_idx

-- DROP INDEX public.audit_opinion_facts_financial_year_idx;

CREATE INDEX audit_opinion_facts_financial_year_idx
  ON public.audit_opinion_facts
  USING btree
  (financial_year COLLATE pg_catalog."default");

-- Index: public.audit_opinion_facts_opinion_code_idx

-- DROP INDEX public.audit_opinion_facts_opinion_code_idx;

CREATE INDEX audit_opinion_facts_opinion_code_idx
  ON public.audit_opinion_facts
  USING btree
  (opinion_code COLLATE pg_catalog."default");

-- Index: public.audit_opinion_facts_opinion_label_idx

-- DROP INDEX public.audit_opinion_facts_opinion_label_idx;

CREATE INDEX audit_opinion_facts_opinion_label_idx
  ON public.audit_opinion_facts
  USING btree
  (opinion_label COLLATE pg_catalog."default");
