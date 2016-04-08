
alter table incexp_labeled add column demarcation_desc text

alter table incexp_labeled add column financial_year text

alter table incexp_labeled rename column period to period_code

alter table incexp_labeled add column period_length text

alter table incexp_labeled add column financial_period text

insert into incexp_labeled (demarcation_code, period_code, function_code, incexp_cde, act_or_bud_amt) select * from incexp

alter table incexp_labeled rename column function_code to function_cde

update incexp_labeled set financial_year = left(period_code, 4)
