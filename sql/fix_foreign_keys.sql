delete from aged_creditor_facts where item_code not in (select code from aged_creditor_items);
ALTER TABLE aged_creditor_facts ADD CONSTRAINT aged_creditor_item_code_fk FOREIGN KEY (item_code) REFERENCES aged_creditor_items (code) MATCH FULL;

delete from aged_debtor_facts where item_code not in (select code from aged_debtor_items);
ALTER TABLE aged_debtor_facts ADD CONSTRAINT aged_debtor_item_code_fk FOREIGN KEY (item_code) REFERENCES aged_debtor_items (code) MATCH FULL;

delete from bsheet_facts where item_code not in (select code from bsheet_items);
ALTER TABLE bsheet_facts ADD CONSTRAINT bsheet_item_code_fk FOREIGN KEY (item_code) REFERENCES bsheet_items (code) MATCH FULL;

delete from capital_facts where item_code not in (select code from capital_items);
ALTER TABLE capital_facts ADD CONSTRAINT capital_item_code_fk FOREIGN KEY (item_code) REFERENCES capital_items (code) MATCH FULL;
ALTER TABLE capital_facts ADD CONSTRAINT capital_function_code_fk FOREIGN KEY (function_code) REFERENCES government_functions (code) MATCH FULL;

\copy cflow_items (code,label) FROM '/home/jdb/Downloads/complete list of codes - cflow old.csv' DELIMITER ',' CSV HEADER;
ALTER TABLE cflow_facts ADD CONSTRAINT cflow_item_code_fk FOREIGN KEY (item_code) REFERENCES cflow_items (code) MATCH FULL;
