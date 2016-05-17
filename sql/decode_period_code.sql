\echo 'aged_creditor'
update aged_creditor_facts set financial_year = cast(left(period_code, 4) as int);
update aged_creditor_facts set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update aged_creditor_facts set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update aged_creditor_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update aged_creditor_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update aged_creditor_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update aged_creditor_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';

\echo 'aged_debtor'
update aged_debtor_facts set financial_year = cast(left(period_code, 4) as int);
update aged_debtor_facts set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update aged_debtor_facts set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update aged_debtor_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update aged_debtor_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update aged_debtor_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update aged_debtor_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';

\echo 'bsheet'
update bsheet_facts set financial_year = cast(left(period_code, 4) as int);
update bsheet_facts set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update bsheet_facts set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update bsheet_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update bsheet_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update bsheet_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update bsheet_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';

\echo 'capital'
update capital_facts set financial_year = cast(left(period_code, 4) as int);
update capital_facts set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update capital_facts set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update capital_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update capital_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update capital_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update capital_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';

\echo 'cflow'
update cflow_facts set financial_year = cast(left(period_code, 4) as int);
update cflow_facts set amount_type_code = substr(period_code, 5, 4) where substr(period_code, 5, 4) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update cflow_facts set amount_type_code = 'ACT' where substr(period_code, 5, 4) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update cflow_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}' and substr(period_code, 9, 3) not similar to 'M\d{2}';
update cflow_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}' or substr(period_code, 9, 3) similar to 'M\d{2}';
update cflow_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month' and amount_type_code = 'ACT';
update cflow_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month' and amount_type_code != 'ACT';
update cflow_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';

\echo 'conditional_grants'
update conditional_grants_facts set financial_year = cast(left(period_code, 4) as int);
update conditional_grants_facts set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD', 'IBY2', 'TRFR', 'SCHD');
update conditional_grants_facts set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update conditional_grants_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update conditional_grants_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update conditional_grants_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update conditional_grants_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';

\echo 'incexp'
update incexp_facts set financial_year = cast(left(period_code, 4) as int);
update incexp_facts set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update incexp_facts set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update incexp_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update incexp_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update incexp_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update incexp_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';

\echo 'repmaint'
update repmaint_facts set financial_year = cast(left(period_code, 4) as int);
update repmaint_facts set amount_type_code = substr(period_code, 5) where substr(period_code, 5) in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update repmaint_facts set amount_type_code = 'ACT' where substr(period_code, 5) not in ('IBY1', 'IBY2', 'ADJB', 'ORGB', 'AUDA', 'PAUD');
update repmaint_facts set period_length = 'year' where substr(period_code, 5, 3) not similar to 'M\d{2}';
update repmaint_facts set period_length = 'month' where substr(period_code, 5, 3) similar to 'M\d{2}';
update repmaint_facts set financial_period = cast(right(period_code, 2) as int) where period_length = 'month';
update repmaint_facts set financial_period = cast(left(period_code, 4) as int) where period_length = 'year';
