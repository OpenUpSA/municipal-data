update cflow_labeled set financial_year = cast(left(period_code, 4) as int);
update cflow_labeled set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD', 'IBY2');
update cflow_labeled set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD', 'IBY2');
update cflow_labeled set demarcation_label = sub.label from (select * from demarcation) sub where sub.code = demarcation_code;
update cflow_labeled set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update cflow_labeled set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update cflow_labeled set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update cflow_labeled set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';
update cflow_labeled set amount_type_label = sub.label from (select * from amount_type) as sub where sub.code = amount_type_code;
update cflow_labeled set item_label = subquery.label, position_in_return_form = subquery.position_in_return_form, return_form_structure = subquery.return_form_structure, composition = subquery.composition from (select * from cflow_labels ) as subquery where subquery.code = item_code;

update cflow_labeled set amount_type_code = 'FORECAST' where period_length = 'month' and financial_year = 2016 and amount_type_code = 'ACT';
update cflow_labeled set amount_type_label = 'Forecast' where period_length = 'month' and financial_year = 2016 and amount_type_code = 'FORECAST';
