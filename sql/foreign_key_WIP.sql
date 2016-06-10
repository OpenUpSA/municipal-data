alter table aged_creditor_facts  add CONSTRAINT item_code_fk FOREIGN KEY (item_code) REFERENCES aged_creditor_items (code) MATCH FULL;


 select demarcation_code, period_code, item_code from aged_creditor_facts where item_code in ('DC42', 'Mas/');


alter table aged_debtor_facts  add CONSTRAINT item_code_fk FOREIGN KEY (item_code) REFERENCES aged_debtor_items (code) MATCH FULL;
c
select demarcation_code, period_code, item_code from aged_debtor_facts where item_code not in (select code from aged_debtor_items);
