BEGIN;

CREATE TEMPORARY TABLE municipalities_update
(
demarcation_code TEXT,
postal_address_1 TEXT,
postal_address_2 TEXT,
postal_address_3 TEXT,
street_address_1 TEXT,
street_address_2 TEXT,
street_address_3 TEXT,
street_address_4 TEXT,
phone_number TEXT,
fax_number TEXT,
url TEXT
) ON COMMIT DROP;

\copy municipalities_update (demarcation_code,postal_address_1,postal_address_2,postal_address_3,street_address_1,street_address_2,street_address_3,street_address_4,phone_number,fax_number,url) FROM '/home/jdb/proj/code4sa/municipal_finance/django-app/muni_contacts.csv' DELIMITER ',' CSV HEADER;

update scorecard_geography g
set
  postal_address_1 = m.postal_address_1,
  postal_address_2 = m.postal_address_2,
  postal_address_3 = m.postal_address_3,
  street_address_1 = m.street_address_1,
  street_address_2 = m.street_address_2,
  street_address_3 = m.street_address_3,
  street_address_4 = m.street_address_4,
  phone_number = m.phone_number,
  fax_number = m.fax_number,
  url = m.url
from municipalities_update m
where g.geo_code = m.demarcation_code;

CREATE TEMPORARY TABLE municipalities_miif_update
(
demarcation_code TEXT,
miif_code TEXT
) ON COMMIT DROP;

\copy municipalities_miif_update (demarcation_code,miif_code) FROM '/home/jdb/proj/code4sa/municipal_finance/datasets/2017q1/demarcation-changes/miif_code.csv' DELIMITER ',' CSV HEADER;

update scorecard_geography g
set
  miif_category = m.miif_code
from municipalities_miif_update m
where g.geo_code = m.demarcation_code;

COMMIT;
