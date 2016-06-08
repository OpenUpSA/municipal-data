create table repmaint_facts_import as select * from repmaint_facts limit 0;
create table incexp_facts_import as select * from incecp_facts limit 0;
create table cflow_facts_import as select * from cflow_facts limit 0;
create table capital_facts_import as select * from capital_facts limit 0;
create table bsheet_facts_import as select * from bsheet_facts limit 0;
create table aged_debtor_facts_import as select * from aged_debtor_facts limit 0;
create table aged_creditor_facts_import as select * from aged_creditor_facts limit 0;

\copy repmaint_facts_import (demarcation_code, period_code, item_code, amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/all_muni/rm_2014q4_acrmun.csv' DELIMITER ',' CSV HEADER;

\copy aged_creditor_facts (demarcation_code, period_code, item_code, g1_amount, l1_amount, l120_amount, l150_amount, l180_amount, l30_amount, l60_amount, l90_amount, total_amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/all_muni/cred_2015q4_acrmun.csv' DELIMITER ',' CSV HEADER;

\copy aged_creditor_facts_import (demarcation_code, period_code, item_code, g1_amount, l1_amount, l120_amount, l150_amount, l180_amount, l30_amount, l60_amount, l90_amount, total_amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/all_muni/cred_2014q4_acrmun.csv' DELIMITER ',' CSV HEADER;

\copy aged_debtor_facts (demarcation_code, period_code, customer_group_code, item_code, bad_amount, badi_amount, g1_amount, l1_amount, l120_amount, l150_amount, l180_amount, l30_amount, l60_amount, l90_amount, total_amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/all_muni/debt_2015q4_acrmun.csv' DELIMITER ',' CSV HEADER;

\copy aged_debtor_facts_import (demarcation_code, period_code, customer_group_code, item_code, bad_amount, badi_amount, g1_amount, l1_amount, l120_amount, l150_amount, l180_amount, l30_amount, l60_amount, l90_amount, total_amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/all_muni/debt_2014q4_acrmun.csv' DELIMITER ',' CSV HEADER;

\copy bsheet_facts (demarcation_code, period_code, item_code, amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/all_muni/bsheet_2015q4_acrmun.csv' DELIMITER ',' CSV HEADER;

\copy bsheet_facts_import (demarcation_code, period_code, item_code, amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/all_muni/bsheet_2014q4_acrmun.csv' DELIMITER ',' CSV HEADER;

\copy capital_facts (demarcation_code, period_code, function_code, item_code, new_assets, renewal_of_existing, total_assets, repairs_maintenance, asset_register_summary) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/all_muni/capital_2015q4_acrmun.csv' DELIMITER ',' CSV HEADER;

\copy capital_facts_import (demarcation_code, period_code, function_code, item_code, new_assets, renewal_of_existing, total_assets, repairs_maintenance, asset_register_summary) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/all_muni/capital_2014q4_acrmun.csv' DELIMITER ',' CSV HEADER;

insert into repmaint_facts (demarcation_code, period_code, item_code, amount)
(select i.demarcation_code, i.period_code, i.item_code, i.amount
from repmaint_facts l right join repmaint_facts_import i on
 l.demarcation_code=i.demarcation_code
and l.period_code=i.period_code
and l.item_code=i.item_code
where l.demarcation_code is null);

insert into aged_creditor_facts (demarcation_code, period_code, item_code, g1_amount, l1_amount, l120_amount, l150_amount, l180_amount, l30_amount, l60_amount, l90_amount, total_amount)
(select i.demarcation_code, i.period_code, i.item_code, i.g1_amount, i.l1_amount, i.l120_amount, i.l150_amount, i.l180_amount, i.l30_amount, i.l60_amount, i.l90_amount, i.total_amount
from aged_creditor_facts l right join aged_creditor_facts_import i on
 l.demarcation_code=i.demarcation_code
and l.period_code=i.period_code
and l.item_code=i.item_code
where l.demarcation_code is null);

insert into aged_debtor_facts (demarcation_code, period_code, customer_group_code, item_code, bad_amount, badi_amount, g1_amount, l1_amount, l120_amount, l150_amount, l180_amount, l30_amount, l60_amount, l90_amount, total_amount)
(select i.demarcation_code, i.period_code, i.customer_group_code, i.item_code, i.bad_amount, i.badi_amount, i.g1_amount, i.l1_amount, i.l120_amount, i.l150_amount, i.l180_amount, i.l30_amount, i.l60_amount, i.l90_amount, i.total_amount
from aged_debtor_facts l right join aged_debtor_facts_import i on
 l.demarcation_code=i.demarcation_code
and l.period_code=i.period_code
and l.item_code=i.item_code
and l.customer_group_code = i.customer_group_code
where l.demarcation_code is null);

insert into bsheet_facts (demarcation_code, period_code, item_code, amount)
(select i.demarcation_code, i.period_code, i.item_code, i.amount
from bsheet_facts l right join bsheet_facts_import i on
 l.demarcation_code=i.demarcation_code
and l.period_code=i.period_code
and l.item_code=i.item_code
where l.demarcation_code is null);

insert into capital_facts (demarcation_code, period_code, function_code, item_code, new_assets, renewal_of_existing, total_assets, repairs_maintenance, asset_register_summary)
(select i.demarcation_code, i.period_code, i.function_code, i.item_code, i.new_assets, i.renewal_of_existing, i.total_assets, i.repairs_maintenance, i.asset_register_summary
from capital_facts l right join capital_facts_import i on
 l.demarcation_code=i.demarcation_code
and l.period_code=i.period_code
and l.function_code = i.function_code
and l.item_code=i.item_code
where l.demarcation_code is null);
