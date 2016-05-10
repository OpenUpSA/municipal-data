update cflow_labeled set financial_year = (left(period_code, 4))::int;

update cflow_labeled set item_label = subquery.description from (select * from codes_desc ) as subquery where subquery.column_name = 'CFLOW_CDE' and subquery.code = item_code;

update cflow_labeled set demarcation_label = sub.label from (select * from demarcation) as sub where sub.code = demarcation_code;

update cflow_labeled set period_length = 'year' where right(left(period_code, 5), 1) != 'M';
update cflow_labeled set period_length = 'month' where right(left(period_code, 5), 1) = 'M';

update cflow_labeled set financial_period = right(period_code, 2) where period_length = 'month';
update cflow_labeled set financial_period = left(period_code, 4) where period_length = 'year';

update cflow_labeled set amount_type_label = sub.label from (select * from amount_type) as sub where sub.code = amount_type_code;


update cflow_labeled set amount_type_code = 'FORECAST' where period_length = 'month' and financial_year = 2016 and amount_type_code = 'ACT';
update cflow_labeled set amount_type_label = 'Forecast' where period_length = 'month' and financial_year = 2016 and amount_type_code = 'FORECAST';

update cflow_labeled set position_in_return_form = subquery.position_in_return_form, return_form_structure = subquery.return_form_structure, composition = subquery.composition from (select * from cflow_labels ) as subquery where subquery.code = item_code;
