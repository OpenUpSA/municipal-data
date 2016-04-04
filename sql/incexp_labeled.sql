create table incexp_labeled4 as
  select demarcation_code,
         period,
         function_code,
         function_desc,
         incexp_cde,
         codes_desc.description as description,
         act_or_bud_amt
  from (
    select incexp.demarcation_code as demarcation_code,
           incexp.period as period,
           incexp.function_cde as function_code,
           codes_desc.description as function_desc,
           incexp.incexp_cde as incexp_cde,
           incexp.act_or_bud as act_or_bud_amt
    from incexp
    inner join codes_desc
      on (incexp.function_cde = codes_desc.code and
          codes_desc.column_name = 'FUNCTION_CDE')
  ) as inc_exp_func_desc
  inner join codes_desc
    on (codes_desc.code = inc_exp_func_desc.incexp_cde and
        codes_desc.column_name = 'INCEXP_CDE')
