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
from municipality_contacts m
where g.geo_code = m.demarcation_code;
