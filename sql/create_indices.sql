\echo cube=repmaint
\echo dimension=amount_type
\echo attributes
CREATE INDEX amount_type_code_idx ON amount_type (code);
CREATE INDEX amount_type_label_idx ON amount_type (label);
\echo dimension
CREATE INDEX amount_type_dimension_amount_type_idx ON amount_type (code, label);
\echo join column
CREATE INDEX repmaint_facts_dimension_join_column_amount_type_idx ON repmaint_facts (amount_type_code);
\echo dimension=demarcation
\echo attributes
CREATE INDEX scorecard_geography_geo_code_idx ON scorecard_geography (geo_code);
CREATE INDEX scorecard_geography_name_idx ON scorecard_geography (name);
\echo dimension
CREATE INDEX scorecard_geography_dimension_demarcation_idx ON scorecard_geography (geo_code, name);
\echo join column
CREATE INDEX repmaint_facts_dimension_join_column_demarcation_idx ON repmaint_facts (demarcation_code);
\echo dimension=period_length
\echo attributes
CREATE INDEX repmaint_facts_period_length_idx ON repmaint_facts (period_length);
\echo dimension=item
\echo attributes
CREATE INDEX repmaint_items_position_in_return_form_idx ON repmaint_items (position_in_return_form);
CREATE INDEX repmaint_items_code_idx ON repmaint_items (code);
CREATE INDEX repmaint_items_return_form_structure_idx ON repmaint_items (return_form_structure);
CREATE INDEX repmaint_items_composition_idx ON repmaint_items (composition);
CREATE INDEX repmaint_items_label_idx ON repmaint_items (label);
\echo dimension
CREATE INDEX repmaint_items_dimension_item_idx ON repmaint_items (code, composition, label, position_in_return_form, return_form_structure);
\echo join column
CREATE INDEX repmaint_facts_dimension_join_column_item_idx ON repmaint_facts (item_code);
\echo dimension positional
CREATE INDEX repmaint_items_position_ordered_idx ON repmaint_items (position_in_return_form, code, composition, label, return_form_structure);
\echo dimension=financial_period
\echo attributes
CREATE INDEX repmaint_facts_financial_period_idx ON repmaint_facts (financial_period);
\echo dimension=financial_year_end
\echo attributes
CREATE INDEX repmaint_facts_financial_year_idx ON repmaint_facts (financial_year);
\echo cube=aged_creditor
\echo dimension=amount_type
\echo attributes
CREATE INDEX amount_type_code_idx ON amount_type (code);
CREATE INDEX amount_type_label_idx ON amount_type (label);
\echo dimension
CREATE INDEX amount_type_dimension_amount_type_idx ON amount_type (code, label);
\echo join column
CREATE INDEX aged_creditor_facts_dimension_join_column_amount_type_idx ON aged_creditor_facts (amount_type_code);
\echo dimension=demarcation
\echo attributes
CREATE INDEX scorecard_geography_geo_code_idx ON scorecard_geography (geo_code);
CREATE INDEX scorecard_geography_name_idx ON scorecard_geography (name);
\echo dimension
CREATE INDEX scorecard_geography_dimension_demarcation_idx ON scorecard_geography (geo_code, name);
\echo join column
CREATE INDEX aged_creditor_facts_dimension_join_column_demarcation_idx ON aged_creditor_facts (demarcation_code);
\echo dimension=period_length
\echo attributes
CREATE INDEX aged_creditor_facts_period_length_idx ON aged_creditor_facts (period_length);
\echo dimension=item
\echo attributes
CREATE INDEX aged_creditor_items_position_in_return_form_idx ON aged_creditor_items (position_in_return_form);
CREATE INDEX aged_creditor_items_code_idx ON aged_creditor_items (code);
CREATE INDEX aged_creditor_items_return_form_structure_idx ON aged_creditor_items (return_form_structure);
CREATE INDEX aged_creditor_items_composition_idx ON aged_creditor_items (composition);
CREATE INDEX aged_creditor_items_label_idx ON aged_creditor_items (label);
\echo dimension
CREATE INDEX aged_creditor_items_dimension_item_idx ON aged_creditor_items (code, composition, label, position_in_return_form, return_form_structure);
\echo join column
CREATE INDEX aged_creditor_facts_dimension_join_column_item_idx ON aged_creditor_facts (item_code);
\echo dimension positional
CREATE INDEX aged_creditor_items_position_ordered_idx ON aged_creditor_items (position_in_return_form, code, composition, label, return_form_structure);
\echo dimension=financial_period
\echo attributes
CREATE INDEX aged_creditor_facts_financial_period_idx ON aged_creditor_facts (financial_period);
\echo dimension=financial_year_end
\echo attributes
CREATE INDEX aged_creditor_facts_financial_year_idx ON aged_creditor_facts (financial_year);
\echo cube=incexp
\echo dimension=function
\echo attributes
CREATE INDEX government_functions_code_idx ON government_functions (code);
CREATE INDEX government_functions_label_idx ON government_functions (label);
\echo dimension
CREATE INDEX government_functions_dimension_function_idx ON government_functions (code, label);
\echo join column
CREATE INDEX incexp_facts_dimension_join_column_function_idx ON incexp_facts (function_code);
\echo dimension=amount_type
\echo attributes
CREATE INDEX amount_type_code_idx ON amount_type (code);
CREATE INDEX amount_type_label_idx ON amount_type (label);
\echo dimension
CREATE INDEX amount_type_dimension_amount_type_idx ON amount_type (code, label);
\echo join column
CREATE INDEX incexp_facts_dimension_join_column_amount_type_idx ON incexp_facts (amount_type_code);
\echo dimension=demarcation
\echo attributes
CREATE INDEX scorecard_geography_geo_code_idx ON scorecard_geography (geo_code);
CREATE INDEX scorecard_geography_name_idx ON scorecard_geography (name);
\echo dimension
CREATE INDEX scorecard_geography_dimension_demarcation_idx ON scorecard_geography (geo_code, name);
\echo join column
CREATE INDEX incexp_facts_dimension_join_column_demarcation_idx ON incexp_facts (demarcation_code);
\echo dimension=period_length
\echo attributes
CREATE INDEX incexp_facts_period_length_idx ON incexp_facts (period_length);
\echo dimension=item
\echo attributes
CREATE INDEX incexp_items_position_in_return_form_idx ON incexp_items (position_in_return_form);
CREATE INDEX incexp_items_code_idx ON incexp_items (code);
CREATE INDEX incexp_items_return_form_structure_idx ON incexp_items (return_form_structure);
CREATE INDEX incexp_items_composition_idx ON incexp_items (composition);
CREATE INDEX incexp_items_label_idx ON incexp_items (label);
\echo dimension
CREATE INDEX incexp_items_dimension_item_idx ON incexp_items (code, composition, label, position_in_return_form, return_form_structure);
\echo join column
CREATE INDEX incexp_facts_dimension_join_column_item_idx ON incexp_facts (item_code);
\echo dimension positional
CREATE INDEX incexp_items_position_ordered_idx ON incexp_items (position_in_return_form, code, composition, label, return_form_structure);
\echo dimension=financial_period
\echo attributes
CREATE INDEX incexp_facts_financial_period_idx ON incexp_facts (financial_period);
\echo dimension=financial_year_end
\echo attributes
CREATE INDEX incexp_facts_financial_year_idx ON incexp_facts (financial_year);
\echo cube=conditional_grants
\echo dimension=amount_type
\echo attributes
CREATE INDEX amount_type_code_idx ON amount_type (code);
CREATE INDEX amount_type_label_idx ON amount_type (label);
\echo dimension
CREATE INDEX amount_type_dimension_amount_type_idx ON amount_type (code, label);
\echo join column
CREATE INDEX conditional_grants_facts_dimension_join_column_amount_type_idx ON conditional_grants_facts (amount_type_code);
\echo dimension=demarcation
\echo attributes
CREATE INDEX scorecard_geography_geo_code_idx ON scorecard_geography (geo_code);
CREATE INDEX scorecard_geography_name_idx ON scorecard_geography (name);
\echo dimension
CREATE INDEX scorecard_geography_dimension_demarcation_idx ON scorecard_geography (geo_code, name);
\echo join column
CREATE INDEX conditional_grants_facts_dimension_join_column_demarcation_idx ON conditional_grants_facts (demarcation_code);
\echo dimension=grant
\echo attributes
CREATE INDEX conditional_grants_code_idx ON conditional_grants (code);
CREATE INDEX conditional_grants_name_idx ON conditional_grants (name);
\echo dimension
CREATE INDEX conditional_grants_dimension_grant_idx ON conditional_grants (code, name);
\echo join column
CREATE INDEX conditional_grants_facts_dimension_join_column_grant_idx ON conditional_grants_facts (grant_code);
\echo dimension=period_length
\echo attributes
CREATE INDEX conditional_grants_facts_period_length_idx ON conditional_grants_facts (period_length);
\echo dimension=financial_period
\echo attributes
CREATE INDEX conditional_grants_facts_financial_period_idx ON conditional_grants_facts (financial_period);
\echo dimension=financial_year_end
\echo attributes
CREATE INDEX conditional_grants_facts_financial_year_idx ON conditional_grants_facts (financial_year);
\echo cube=bsheet
\echo dimension=amount_type
\echo attributes
CREATE INDEX amount_type_code_idx ON amount_type (code);
CREATE INDEX amount_type_label_idx ON amount_type (label);
\echo dimension
CREATE INDEX amount_type_dimension_amount_type_idx ON amount_type (code, label);
\echo join column
CREATE INDEX bsheet_facts_dimension_join_column_amount_type_idx ON bsheet_facts (amount_type_code);
\echo dimension=demarcation
\echo attributes
CREATE INDEX scorecard_geography_geo_code_idx ON scorecard_geography (geo_code);
CREATE INDEX scorecard_geography_name_idx ON scorecard_geography (name);
\echo dimension
CREATE INDEX scorecard_geography_dimension_demarcation_idx ON scorecard_geography (geo_code, name);
\echo join column
CREATE INDEX bsheet_facts_dimension_join_column_demarcation_idx ON bsheet_facts (demarcation_code);
\echo dimension=period_length
\echo attributes
CREATE INDEX bsheet_facts_period_length_idx ON bsheet_facts (period_length);
\echo dimension=item
\echo attributes
CREATE INDEX bsheet_items_position_in_return_form_idx ON bsheet_items (position_in_return_form);
CREATE INDEX bsheet_items_code_idx ON bsheet_items (code);
CREATE INDEX bsheet_items_return_form_structure_idx ON bsheet_items (return_form_structure);
CREATE INDEX bsheet_items_composition_idx ON bsheet_items (composition);
CREATE INDEX bsheet_items_label_idx ON bsheet_items (label);
\echo dimension
CREATE INDEX bsheet_items_dimension_item_idx ON bsheet_items (code, composition, label, position_in_return_form, return_form_structure);
\echo join column
CREATE INDEX bsheet_facts_dimension_join_column_item_idx ON bsheet_facts (item_code);
\echo dimension positional
CREATE INDEX bsheet_items_position_ordered_idx ON bsheet_items (position_in_return_form, code, composition, label, return_form_structure);
\echo dimension=financial_period
\echo attributes
CREATE INDEX bsheet_facts_financial_period_idx ON bsheet_facts (financial_period);
\echo dimension=financial_year_end
\echo attributes
CREATE INDEX bsheet_facts_financial_year_idx ON bsheet_facts (financial_year);
\echo cube=cflow
\echo dimension=amount_type
\echo attributes
CREATE INDEX amount_type_code_idx ON amount_type (code);
CREATE INDEX amount_type_label_idx ON amount_type (label);
\echo dimension
CREATE INDEX amount_type_dimension_amount_type_idx ON amount_type (code, label);
\echo join column
CREATE INDEX cflow_facts_dimension_join_column_amount_type_idx ON cflow_facts (amount_type_code);
\echo dimension=demarcation
\echo attributes
CREATE INDEX scorecard_geography_geo_code_idx ON scorecard_geography (geo_code);
CREATE INDEX scorecard_geography_name_idx ON scorecard_geography (name);
\echo dimension
CREATE INDEX scorecard_geography_dimension_demarcation_idx ON scorecard_geography (geo_code, name);
\echo join column
CREATE INDEX cflow_facts_dimension_join_column_demarcation_idx ON cflow_facts (demarcation_code);
\echo dimension=period_length
\echo attributes
CREATE INDEX cflow_facts_period_length_idx ON cflow_facts (period_length);
\echo dimension=item
\echo attributes
CREATE INDEX cflow_items_position_in_return_form_idx ON cflow_items (position_in_return_form);
CREATE INDEX cflow_items_code_idx ON cflow_items (code);
CREATE INDEX cflow_items_return_form_structure_idx ON cflow_items (return_form_structure);
CREATE INDEX cflow_items_composition_idx ON cflow_items (composition);
CREATE INDEX cflow_items_label_idx ON cflow_items (label);
\echo dimension
CREATE INDEX cflow_items_dimension_item_idx ON cflow_items (code, composition, label, position_in_return_form, return_form_structure);
\echo join column
CREATE INDEX cflow_facts_dimension_join_column_item_idx ON cflow_facts (item_code);
\echo dimension positional
CREATE INDEX cflow_items_position_ordered_idx ON cflow_items (position_in_return_form, code, composition, label, return_form_structure);
\echo dimension=financial_period
\echo attributes
CREATE INDEX cflow_facts_financial_period_idx ON cflow_facts (financial_period);
\echo dimension=financial_year_end
\echo attributes
CREATE INDEX cflow_facts_financial_year_idx ON cflow_facts (financial_year);
\echo cube=officials
\echo dimension=municipality
\echo attributes
CREATE INDEX municipality_contacts_demarcation_code_idx ON municipality_contacts (demarcation_code);
\echo dimension=role
\echo attributes
CREATE INDEX municipality_contacts_role_idx ON municipality_contacts (role);
\echo dimension=contact_details
\echo attributes
CREATE INDEX municipality_contacts_office_number_idx ON municipality_contacts (office_number);
CREATE INDEX municipality_contacts_title_idx ON municipality_contacts (title);
CREATE INDEX municipality_contacts_email_address_idx ON municipality_contacts (email_address);
CREATE INDEX municipality_contacts_fax_number_idx ON municipality_contacts (fax_number);
CREATE INDEX municipality_contacts_name_idx ON municipality_contacts (name);
\echo dimension
CREATE INDEX municipality_contacts_dimension_contact_details_idx ON municipality_contacts (email_address, fax_number, name, office_number, title);
\echo cube=aged_debtor
\echo dimension=amount_type
\echo attributes
CREATE INDEX amount_type_code_idx ON amount_type (code);
CREATE INDEX amount_type_label_idx ON amount_type (label);
\echo dimension
CREATE INDEX amount_type_dimension_amount_type_idx ON amount_type (code, label);
\echo join column
CREATE INDEX aged_debtor_facts_dimension_join_column_amount_type_idx ON aged_debtor_facts (amount_type_code);
\echo dimension=demarcation
\echo attributes
CREATE INDEX scorecard_geography_geo_code_idx ON scorecard_geography (geo_code);
CREATE INDEX scorecard_geography_name_idx ON scorecard_geography (name);
\echo dimension
CREATE INDEX scorecard_geography_dimension_demarcation_idx ON scorecard_geography (geo_code, name);
\echo join column
CREATE INDEX aged_debtor_facts_dimension_join_column_demarcation_idx ON aged_debtor_facts (demarcation_code);
\echo dimension=period_length
\echo attributes
CREATE INDEX aged_debtor_facts_period_length_idx ON aged_debtor_facts (period_length);
\echo dimension=customer_group
\echo attributes
CREATE INDEX aged_debtor_facts_customer_group_code_idx ON aged_debtor_facts (customer_group_code);
\echo dimension=item
\echo attributes
CREATE INDEX aged_debtor_items_position_in_return_form_idx ON aged_debtor_items (position_in_return_form);
CREATE INDEX aged_debtor_items_code_idx ON aged_debtor_items (code);
CREATE INDEX aged_debtor_items_return_form_structure_idx ON aged_debtor_items (return_form_structure);
CREATE INDEX aged_debtor_items_composition_idx ON aged_debtor_items (composition);
CREATE INDEX aged_debtor_items_label_idx ON aged_debtor_items (label);
\echo dimension
CREATE INDEX aged_debtor_items_dimension_item_idx ON aged_debtor_items (code, composition, label, position_in_return_form, return_form_structure);
\echo join column
CREATE INDEX aged_debtor_facts_dimension_join_column_item_idx ON aged_debtor_facts (item_code);
\echo dimension positional
CREATE INDEX aged_debtor_items_position_ordered_idx ON aged_debtor_items (position_in_return_form, code, composition, label, return_form_structure);
\echo dimension=financial_period
\echo attributes
CREATE INDEX aged_debtor_facts_financial_period_idx ON aged_debtor_facts (financial_period);
\echo dimension=financial_year_end
\echo attributes
CREATE INDEX aged_debtor_facts_financial_year_idx ON aged_debtor_facts (financial_year);
\echo cube=municipalities
\echo dimension=municipality
\echo attributes
CREATE INDEX scorecard_geography_category_idx ON scorecard_geography (category);
CREATE INDEX scorecard_geography_province_code_idx ON scorecard_geography (province_code);
CREATE INDEX scorecard_geography_name_idx ON scorecard_geography (name);
CREATE INDEX scorecard_geography_url_idx ON scorecard_geography (url);
CREATE INDEX scorecard_geography_street_address_4_idx ON scorecard_geography (street_address_4);
CREATE INDEX scorecard_geography_street_address_1_idx ON scorecard_geography (street_address_1);
CREATE INDEX scorecard_geography_fax_number_idx ON scorecard_geography (fax_number);
CREATE INDEX scorecard_geography_street_address_3_idx ON scorecard_geography (street_address_3);
CREATE INDEX scorecard_geography_street_address_2_idx ON scorecard_geography (street_address_2);
CREATE INDEX scorecard_geography_long_name_idx ON scorecard_geography (long_name);
CREATE INDEX scorecard_geography_postal_address_1_idx ON scorecard_geography (postal_address_1);
CREATE INDEX scorecard_geography_postal_address_3_idx ON scorecard_geography (postal_address_3);
CREATE INDEX scorecard_geography_postal_address_2_idx ON scorecard_geography (postal_address_2);
CREATE INDEX scorecard_geography_parent_code_idx ON scorecard_geography (parent_code);
CREATE INDEX scorecard_geography_phone_number_idx ON scorecard_geography (phone_number);
CREATE INDEX scorecard_geography_province_name_idx ON scorecard_geography (province_name);
CREATE INDEX scorecard_geography_geo_code_idx ON scorecard_geography (geo_code);
\echo dimension
CREATE INDEX scorecard_geography_dimension_municipality_idx ON scorecard_geography (category, geo_code, fax_number, long_name, name, parent_code, phone_number, postal_address_1, postal_address_2, postal_address_3, province_code, province_name, street_address_1, street_address_2, street_address_3, street_address_4, url);
\echo cube=audit_opinions
\echo dimension=opinion
\echo attributes
CREATE INDEX audit_opinion_facts_opinion_code_idx ON audit_opinion_facts (opinion_code);
CREATE INDEX audit_opinion_facts_opinion_label_idx ON audit_opinion_facts (opinion_label);
\echo dimension
CREATE INDEX audit_opinion_facts_dimension_opinion_idx ON audit_opinion_facts (opinion_code, opinion_label);
\echo dimension=demarcation
\echo attributes
CREATE INDEX scorecard_geography_geo_code_idx ON scorecard_geography (geo_code);
CREATE INDEX scorecard_geography_name_idx ON scorecard_geography (name);
\echo dimension
CREATE INDEX scorecard_geography_dimension_demarcation_idx ON scorecard_geography (geo_code, name);
\echo join column
CREATE INDEX audit_opinion_facts_dimension_join_column_demarcation_idx ON audit_opinion_facts (demarcation_code);
\echo dimension=financial_year_end
\echo attributes
CREATE INDEX audit_opinion_facts_financial_year_idx ON audit_opinion_facts (financial_year);
\echo cube=capital
\echo dimension=function
\echo attributes
CREATE INDEX government_functions_code_idx ON government_functions (code);
CREATE INDEX government_functions_label_idx ON government_functions (label);
\echo dimension
CREATE INDEX government_functions_dimension_function_idx ON government_functions (code, label);
\echo join column
CREATE INDEX capital_facts_dimension_join_column_function_idx ON capital_facts (function_code);
\echo dimension=amount_type
\echo attributes
CREATE INDEX amount_type_code_idx ON amount_type (code);
CREATE INDEX amount_type_label_idx ON amount_type (label);
\echo dimension
CREATE INDEX amount_type_dimension_amount_type_idx ON amount_type (code, label);
\echo join column
CREATE INDEX capital_facts_dimension_join_column_amount_type_idx ON capital_facts (amount_type_code);
\echo dimension=demarcation
\echo attributes
CREATE INDEX scorecard_geography_geo_code_idx ON scorecard_geography (geo_code);
CREATE INDEX scorecard_geography_name_idx ON scorecard_geography (name);
\echo dimension
CREATE INDEX scorecard_geography_dimension_demarcation_idx ON scorecard_geography (geo_code, name);
\echo join column
CREATE INDEX capital_facts_dimension_join_column_demarcation_idx ON capital_facts (demarcation_code);
\echo dimension=period_length
\echo attributes
CREATE INDEX capital_facts_period_length_idx ON capital_facts (period_length);
\echo dimension=item
\echo attributes
CREATE INDEX capital_items_position_in_return_form_idx ON capital_items (position_in_return_form);
CREATE INDEX capital_items_code_idx ON capital_items (code);
CREATE INDEX capital_items_return_form_structure_idx ON capital_items (return_form_structure);
CREATE INDEX capital_items_composition_idx ON capital_items (composition);
CREATE INDEX capital_items_label_idx ON capital_items (label);
\echo dimension
CREATE INDEX capital_items_dimension_item_idx ON capital_items (code, composition, label, position_in_return_form, return_form_structure);
\echo join column
CREATE INDEX capital_facts_dimension_join_column_item_idx ON capital_facts (item_code);
\echo dimension positional
CREATE INDEX capital_items_position_ordered_idx ON capital_items (position_in_return_form, code, composition, label, return_form_structure);
\echo dimension=financial_period
\echo attributes
CREATE INDEX capital_facts_financial_period_idx ON capital_facts (financial_period);
\echo dimension=financial_year_end
\echo attributes
CREATE INDEX capital_facts_financial_year_idx ON capital_facts (financial_year);

