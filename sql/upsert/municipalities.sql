BEGIN;

CREATE TEMPORARY TABLE municipality_contacts_upsert
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

\copy municipality_contacts_upsert (demarcation_code,postal_address_1,postal_address_2,postal_address_3,street_address_1,street_address_2,street_address_3,street_address_4,phone_number,fax_number,url) FROM '/home/jdb/projects/municipal-money/municipal-data/muni.csv' DELIMITER ',' CSV HEADER;

UPDATE scorecard_geography f
SET
postal_address_1 = i.postal_address_1,
postal_address_2 = i.postal_address_2,
postal_address_3 = i.postal_address_3,
street_address_1 = i.street_address_1,
street_address_2 = i.street_address_2,
street_address_3 = i.street_address_3,
street_address_4 = i.street_address_4,
phone_number = i.phone_number,
fax_number = i.fax_number,
url = i.url
FROM municipality_contacts_upsert i
WHERE f.geo_code = i.demarcation_code;

COMMIT;
