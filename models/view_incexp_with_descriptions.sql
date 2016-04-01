-- View: public.inc_exp_with_descriptions

-- DROP VIEW public.inc_exp_with_descriptions;

CREATE OR REPLACE VIEW public.inc_exp_with_descriptions AS
 SELECT inc_exp_func_desc.demarcation_code,
    inc_exp_func_desc.period,
    inc_exp_func_desc.function_code,
    inc_exp_func_desc.function_desc,
    inc_exp_func_desc.incexp_cde,
    inc_exp_func_desc.act_or_bud_amt,
    codes_desc.column_name,
    codes_desc.code,
    codes_desc.description
   FROM ( SELECT incexp.demarcation_code,
            incexp.period,
            incexp.function_cde AS function_code,
            codes_desc_1.description AS function_desc,
            incexp.incexp_cde,
            incexp.act_or_bud AS act_or_bud_amt
           FROM incexp
             JOIN codes_desc codes_desc_1 ON incexp.function_cde = codes_desc_1.code
          WHERE codes_desc_1.column_name = 'FUNCTION_CDE'::text) inc_exp_func_desc
     JOIN codes_desc ON codes_desc.code = inc_exp_func_desc.incexp_cde
  WHERE codes_desc.column_name = 'INCEXP_CDE'::text;

ALTER TABLE public.inc_exp_with_descriptions
  OWNER TO postgres;
