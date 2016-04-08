
alter table incexp_labeled add column demarcation_desc text

alter table incexp_labeled add column financial_year text

alter table incexp_labeled rename column period to period_code

alter table incexp_labeled add column period_length text

alter table incexp_labeled add column financial_period text

insert into incexp_labeled (demarcation_code, period_code, function_code, incexp_cde, act_or_bud_amt) select * from incexp

alter table incexp_labeled rename column function_code to function_cde

update incexp_labeled set financial_year = left(period_code, 4)

alter table incexp_labeled add column amount_type_desc text
alter table incexp_labeled add column amount_type_cde text

update incexp_labeled set amount_type_cde = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD', 'IBY2')

update incexp_labeled set amount_type_cde = 'ACT' where amount_type_cde is null

update incexp_labeled set function_desc = subquery.description from (select * from codes_desc ) as subquery where subquery.column_name = 'FUNCTION_CDE' and subquery.code = function_cde

alter table incexp_labeled rename column description to incexp_desc

update incexp_labeled set incexp_desc = subquery.description from (select * from codes_desc ) as subquery where subquery.column_name = 'INCEXP_CDE' and subquery.code = incexp_cde

update incexp_labeled set demarcation_desc = sub.name from (select * from demarcation) sub where sub.code = demarcation_code

update incexp_labeled set period_length = 'year' where amount_type_cde != 'ACT'
update incexp_labeled set period_length = 'month' where amount_type_cde = 'ACT'

update incexp_labeled set financial_period = right(period_code, 2) where period_length = 'month'
update incexp_labeled set financial_period = left(period_code, 4) where period_length = 'year'

update incexp_labeled set amount_type_desc = sub.name from (select * from amount_type) as sub where sub.code = amount_type_cde
