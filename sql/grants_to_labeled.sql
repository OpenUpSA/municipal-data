update grants_labeled set financial_year = cast(left(period_code, 4) as int);

update grants_labeled set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD', 'IBY2', 'TRFR', 'SCHD');

update grants_labeled set amount_type_code = 'ACT' where amount_type_code is null;

update grants_labeled set grant_name = subquery.name from (select * from grant_names ) as subquery where subquery.code = grant_code;

update grants_labeled set demarcation_label = sub.label from (select * from demarcation) sub where sub.code = demarcation_code;

update grants_labeled set period_length = 'year' where amount_type_code != 'ACT';
update grants_labeled set period_length = 'month' where amount_type_code = 'ACT';

update grants_labeled set financial_period = (right(period_code, 2))::int where period_length = 'month';
update grants_labeled set financial_period = (left(period_code, 4))::int where period_length = 'year';

update grants_labeled set amount_type_label = sub.label from (select * from amount_type) as sub where sub.code = amount_type_code;
