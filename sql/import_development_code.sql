create temporary table development_code (development_code text, demarcation_code text);

\copy development_code (development_code, demarcation_code) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/development_code_2011.csv' DELIMITER ',' CSV HEADER;

update scorecard_geography as sg set development_category = dc.development_code from development_code dc where sg.geo_code = dc.demarcation_code;
