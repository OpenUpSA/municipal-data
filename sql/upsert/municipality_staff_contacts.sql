BEGIN;

CREATE TEMPORARY TABLE municipality_staff_contacts_upsert
(
        demarcation_code TEXT,
        role TEXT,
        title TEXT,
        name TEXT,
        office_number TEXT,
        fax_number TEXT,
        email_address TEXT
) ON COMMIT DROP;

\copy municipality_staff_contacts_upsert (demarcation_code, role, title, name, office_number, fax_number, email_address) FROM '/home/ubuntu/django-project/persons.csv' DELIMITER ',' CSV HEADER;

UPDATE municipality_staff_contacts f
SET title = i.title,
    name = i.name,
    office_number = i.office_number,
    fax_number = i.fax_number,
    email_address = i.email_address
FROM municipality_staff_contacts_upsert i
WHERE f.demarcation_code = i.demarcation_code
AND f.role = i.role;

INSERT INTO municipality_staff_contacts
(
    demarcation_code,
    role,
    title,
    name,
    office_number,
    fax_number,
    email_address
)
SELECT demarcation_code, role, title, name, office_number, fax_number, email_address
FROM municipality_staff_contacts_upsert i
WHERE
    NOT EXISTS (
        SELECT * FROM municipality_staff_contacts f
        WHERE f.demarcation_code = i.demarcation_code
        AND f.role = i.role
    );

COMMIT;
