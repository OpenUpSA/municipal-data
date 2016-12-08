BEGIN;

\copy scorecard_geography (geo_code, geo_level, parent_level, parent_code, province_code, province_name, category, year, name) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2017q1/demarcation-changes/new2016_scorecard_geography.csv' DELIMITER ',' CSV HEADER FORCE NOT NULL name;

COMMIT;
