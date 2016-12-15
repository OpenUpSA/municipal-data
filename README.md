# Municipal Money

Municipal Money is a project between the [South African National Treasury](http://www.treasury.gov.za/) and [Code for South Africa](http://code4sa.org) to
make municipal finance information available to the public. It is made up of a citizen-facing app and an API.

# Local development

1. clone this repo
2. install dependencies: ``pip install -r requirements.txt``
3. create a postgresql user with password ``municipal_finance``: ``createuser municipal_finance -W``
4. create a database: ``createdb municipal_finance -O municipal_finance``
5. install data from somewhere :)
6. run it: ``python manage.py runserver``

# Production

```
dokku config:set municipal-finance DJANGO_DEBUG=False \
                                   DISABLE_COLLECTSTATIC=1 \
                                   DJANGO_SECRET_KEY=... \
                                   NEW_RELIC_APP_NAME=municipal_finance \
                                   NEW_RELIC_LICENSE_KEY=... \
                                   DATABASE_URL=postgres://municipal_finance:...@postgresq....amazonaws.com/municipal_finance
```

# Initial Data Import

Data import is still a fairly manual process leveraging the DB and a few SQL scripts to do the hard work. This is usually done against a local DB, sanity checked with a locally-running instance of the API and some tools built on it, and if everything looks ok, dumped table-by-table with something like `pg_dump "postgres://municipal_finance@localhost/municipal_finance" --table=audit_opinions -O -c --if-exists > audit_opinions.sql` and then loaded into the production database.

1. Create the population table with `cat sql/create/030_population_2011.sql | psql municipal_finance`
2. `python manage.py migrate`
3. Create the tables with `cat sql/create/* | psql municipal_finance`
4. Import the first few columns of the fact tables which are supplied by National Treasury
 - e.g. `psql# \copy incexp(demarcation_code, period_code, function_code, item_code, amount) FROM '/bob/incexp_2015q4.csv' DELIMITER ',' CSV HEADER`
5. Run `sql/decode_period_code.sql` to populate the remaining columns from the period code
  - These should be idempotent so they can simply run again when data is added.
6. Import the dimension table data from `municipal_finance/data_import/dimension_tables`
7. Make sure `create_indices.sql` and its indices are up to date
  - create it with the python module `municiapl_finance.data_import.create_indices`
  - add it to git and run it if it was changed
  - the prod DB doesn't support CREATE INDEX IF NOT EXISTS yet so ignore errors for existing indices unless their columns changed and they need to be manually removed and recreated.

*Remember to run `VACUUM ANALYSE` or REINDEX tables after significant changes to ensure stats are up to date to use indices properly.*

# Standard Operating Procedure

This covers how to keep the data up to date. Each quarter, as new data is released, the following needs to be done to update the data served by the API and the Citizen Scorecard. It's best to do this on a test database first and validate the results before updating the production database.

## Extract CSV datasets from Excel Spreadsheets

Extract CSV datasets from Excel Spreadsheets using the following scripts in `municipal_finance/data_import/`

- audit_opinions.py
- contact_details.py
- uifw_expenditure.py

## Scrape the MFMA website for the Audit Report URLs into a CSV file

Using `municipal_finance/data_import/audit_reports.py`

## Insert/update from CSV files

1. Update the paths in the per-cube files in `sql/upsert/`
2. Execute the files

These files work as follows:

1. Create a temporary table
2. Import the CSV file to the temporary table
4. Delete all rows for which a matching demarcation code and period code occurs in the update dataset
  - e.g. if BUF 2016AUDA is in the update, all BUF 2016AUDA rows will be deleted from the update dataset. That means line items that were removed from the Treasury Local Government Database and aren't in quarterly update datasets will also be removed from the Municipal Data database.
  - if a demarcation code and period code is already in the database and not in the update dataset, it will remain in the Municipal Data database.
5. Insert all rows of the update dataset to the fact table
  -

Update the last-updated date in the model files for each cube in `models/*.json`

Update the materialised view data using `bin/materialised_views.py`:

1. Run with --profiles-from-api to update the muni-specific profile data
2. Run with --calc-medians and --calc-rating-counts to update comparison data based on profile changes.
3. Check what changed using `git diff` and commit commit if changes look right.

## Annual data

Whenever Audited Annual data becomes available (AUDA financial data and Audit Outcomes), adjust the years used by `scorecard/profile_data.py` to include the latest financial year available.

Audit outcomes will be captured in the months following 1 December following the end of the financial year. Audited figures can start being submitted by municipalities to Treasury from this point. That means new audited annual figures can appear from Q2.

Pre-audit figures are captured in the period 3 Aug to 30 Nov after the end of the financial year.

## Quarterly data

Currently, indicators using quarterly data automatically use the latest quarter available.

Quarterly Section 71 submissions are available 2 months after the end of the quarter.

## Validating the data

The aim here is to ensure that the data is in the correct format, and that the import worked correctly, such that the correct values are shown to users of the site. That means the right number is returned, for a given line item, for a given period and municipality. The correct number is defined by what has been published on the MFMA website. Examples of the kind of errors this is trying to catch are different number formats, different line item codes or different data structures which aren't detected by the database constraints, but can be detected by manually comparing the numbers presented to published documents. Therefore this shouldn't be exhaustive - when some numbers in each dataset match expected values, we can infer that the data is imported correctly. Since distinctions aren't made between importing different municipalities, other municipalities should be imported equivalently.

Do each of these for a sample of municipalities. Check some metros, some districts, and some locals. Try to find some doing well and some doing badly. Try to compare some with fairly complete data and some with missing data.

You can use `municipal_finance/data_import/data_audit.py` to generate a CSV showing which data is available for which munis. With this you can find munis lacking specific datasets.

-  Contact details
  -  Check that the website link works
  -  Check that contact details look ok
-  Follow Audit report links on the Scorecard site and check that the link works, and that the opinion in the report matches what is shown on the page. For example, the heading "Basis for Qualified Opinion" seems to be around page 2 or 3 for a _Qualified_ opinion on the page. You can also find the [Audit Reports on the MFMA website](http://mfma.treasury.gov.za/Documents/07.%20Audit%20Reports)
-  Compare Original Budget (ORGB) values to [Adopted Budgets on the MFMA website](http://mfma.treasury.gov.za/Documents/03.%20Budget%20Documentation)
  -  Grants - Not all of them appear in our conditional grant dataset - compare those that do e.g. _Local Government Financial Management Grant_
    - e.g. with `select l.name, f.amount from conditional_grants_facts f, conditional_grants l where f.grant_code = l.code and demarcation_code = 'CPT' and amount_type_code = 'ORGB' and financial_year = 2015 and period_length = 'year' order by l.name;`
    - If some values are close, e.g. 217,498,000 vs 217,548,000, the data is probably loaded correctly
  -  Operating Revenue and expenditure
- Compare Audited (AUDA) values to the [audited financial statements on the MFMA website](http://mfma.treasury.gov.za/Documents/05.%20Annual%20Financial%20Statements)
  - Use the _consolidated_ financial statements where available for municipalities with entities
  - You can compare some values in the Scorecard site and the rest in the Table View
  - Debtor (under Consumer Receivables) and Creditor age analysis can be found in the AFS
  - Make sure to check unauthorised, irregular, fruitless and wasteful expenditure
- Compare in-year values to [Section 71 in-year reports](http://mfma.treasury.gov.za/Media_Releases/s71/Pages/default.aspx)
  - This isn't available in the Table View yet so use the API or the database
    - e.g. `select l.label, l30_amount from aged_debtor_facts f, aged_debtor_items l where f.item_code = l.code and demarcation_code = 'CPT' and financial_year = 2016 and financial_period = 09 and amount_type_code = 'ACT';`
  - Compare the latest available month of a quarter to the quarter value in the report

# Upsert Log

## 2016q4

- Some of the files had amounts ending .00 so to check that simply rounding was ok, I ran `grep -v  '\.00' *|egrep  -v "(capital|cflow|grants|rm_)"` - the excluded files didn't have .00 endings.

# License

MIT License
