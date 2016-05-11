-- Table: public.audit_opinions

-- DROP TABLE public.audit_opinions;

CREATE TABLE public.audit_opinions
(
  demarcation_code text NOT NULL,
  financial_year text NOT NULL,
  opinion_code text NOT NULL,
  opinion_label text NOT NULL,
  CONSTRAINT audit_opinions_demarcation_code_financial_year_key UNIQUE (demarcation_code, financial_year)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.audit_opinions
  OWNER TO municipal_finance;

-- Index: public.audit_opinions_demarcation_code_idx

-- DROP INDEX public.audit_opinions_demarcation_code_idx;

CREATE INDEX audit_opinions_demarcation_code_idx
  ON public.audit_opinions
  USING btree
  (demarcation_code COLLATE pg_catalog."default");

-- Index: public.audit_opinions_financial_year_idx

-- DROP INDEX public.audit_opinions_financial_year_idx;

CREATE INDEX audit_opinions_financial_year_idx
  ON public.audit_opinions
  USING btree
  (financial_year COLLATE pg_catalog."default");

-- Index: public.audit_opinions_opinion_code_idx

-- DROP INDEX public.audit_opinions_opinion_code_idx;

CREATE INDEX audit_opinions_opinion_code_idx
  ON public.audit_opinions
  USING btree
  (opinion_code COLLATE pg_catalog."default");

-- Index: public.audit_opinions_opinion_label_idx

-- DROP INDEX public.audit_opinions_opinion_label_idx;

CREATE INDEX audit_opinions_opinion_label_idx
  ON public.audit_opinions
  USING btree
  (opinion_label COLLATE pg_catalog."default");
