create table repmaint_facts_import as select * from repmaint_facts limit 0;

\copy repmaint_facts_import (demarcation_code, period_code, item_code, amount) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/All municipal data 2013-14/rm_2014q4_acrmun.csv' DELIMITER ',' CSV HEADER;

insert into repmaint_facts (demarcation_code, period_code, item_code, amount)
(select i.demarcation_code, i.period_code, i.item_code, i.amount
from repmaint_facts l right join repmaint_facts_import i on
 l.demarcation_code=i.demarcation_code
and l.period_code=i.period_code
and l.item_code=i.item_code
where l.demarcation_code is null);
