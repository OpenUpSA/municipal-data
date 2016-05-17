update aged_creditor_facts set financial_year = cast(left(period_code, 4) as int);
update aged_creditor_facts set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD', 'IBY2');
update aged_creditor_facts set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD', 'IBY2');
update aged_creditor_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update aged_creditor_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update aged_creditor_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update aged_creditor_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';
