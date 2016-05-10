update repmaint_labeled set financial_year = left(period_code, 4);

update repmaint_labeled set amount_type_cde = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD', 'IBY2');

update repmaint_labeled set amount_type_cde = 'ACT' where amount_type_cde is null;

update repmaint_labeled set item_label = subquery.description from (select * from codes_desc ) as subquery where subquery.column_name = 'A1OTH_CDE' and subquery.code = item_code;

update repmaint_labeled set demarcation_desc = sub.name from (select * from demarcation) sub where sub.code = demarcation_code;

update repmaint_labeled set period_length = 'year' where amount_type_cde != 'ACT';
update repmaint_labeled set period_length = 'month' where amount_type_cde = 'ACT';

update repmaint_labeled set financial_period = right(period_code, 2) where period_length = 'month';
update repmaint_labeled set financial_period = left(period_code, 4) where period_length = 'year';

update repmaint_labeled set amount_type_desc = sub.name from (select * from amount_type) as sub where sub.code = amount_type_cde;
update repmaint_labeled set position_in_return_form = subquery.position_in_return_form, return_form_structure = subquery.return_form_structure, composition = subquery.composition from (select * from repmaint_labels ) as subquery where subquery.code = item_code;
