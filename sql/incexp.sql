-- Table: public.incexp

-- DROP TABLE public.incexp;

CREATE TABLE public.incexp
(
  demarcation_code text NOT NULL,
  period text NOT NULL,
  function_cde text NOT NULL,
  incexp_cde text NOT NULL,
  act_or_bud bigint,
  CONSTRAINT primary_key PRIMARY KEY (demarcation_code, period, function_cde, incexp_cde)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.incexp
  OWNER TO postgres;
