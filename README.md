# Municipal Money

Municipal Money is a project between the [South African National Treasury](http://www.treasury.gov.za/) and [OpenUp](https://openup.org.za) to
make municipal finance information available to the public. It is made up of a citizen-facing app and an API.

In production, the two sites are served by one django instance, using the hostname to determine which site to serve. In development, we use the SITE_ID environment variable to select the site, and run two instances when needed:

| Site                                 | Production URL                         | docker-compose service name | Django Sites ID |
|--------------------------------------|----------------------------------------|-----------------------------|-----------------|
| Public-friendly site                 | https://municipalmoney.gov.za/         | scorecard                   | 2               |
| Data exploration/download UI and API | https://municipaldata.treasury.gov.za/ | portal                      | 3               |

# Local development quick start (with docker-compose)

If you only want to work on the scorecard website. The site will use pre-calculated
financials and link to the production data/API site for detail.

```
docker-compose up -d postgres
docker-compose run --rm scorecard python manage.py migrate
docker-compose run --rm scorecard python manage.py loaddata demo-data
docker-compose up scorecard
```

If you want to run the API and data portallocally using docker-compose you also need to:


1. dump the production database
2. load the production database dump into your docker-compose postgres instance
   (this will take at least 40 minutes) with something like

```
docker-compose -f docker-compose.yml -f docker-compose.portal.yml \
               run --rm -v /home/user/folder-containing-dumpdata/:/data \
               portal pg_restore -h postgres -U municipal_finance -d municipal_finance /data/dumpfile
```
3. run the API and data portal along with the scorecard site with something like

```
docker-compose -f docker-compose.yml -f docker-compose.portal.yml up portal scorecard
```

# Local development (without docker)

1. Clone this repo
2. Create a python virtual environment. ```virtualenv <env_name>```
3. Activate virtual environment ``` source <env_name>/bin/activate```
4. Install dependencies.

   Some python packages require system packages.
   * psycopg2 requires libpq-dev (postgresql development files).
   * gnureadline requires libncurses5-dev (ncurses development files).
   * multiple packages require python development files (python-dev).

   After these packages have being installed the python packages can then be installed. ```pip install -r requiments.txt```
5. Install postgresql and create a user and a database.

   ``createuser municipal_finance -W``

   * -W will prompt to create a password for the user.

   ``createdb municipal_finance -O municipal_finance``

   * -O will give ownership of the database to the municipal_finance user.

6. install data from somewhere :)

7. run it: ``python manage.py runserver``

Note when doing a high request rate locally e.g. during updates, it seems that the above command doesn't release resources quickly enough so use the following for the API server instead

```bash
export DJANGO_SETTINGS_MODULE=municipal_finance.settings
export API_URL=http://localhost:8001/api  # only needed if using the table view against local API
export PRELOAD_CUBES=true
export SITE_ID=3
gunicorn --limit-request-line 7168 --worker-class gevent municipal_finance.wsgi:application -t 600 --log-file -
```


# Production

```
dokku config:set municipal-finance DJANGO_DEBUG=False \
                                   DISABLE_COLLECTSTATIC=1 \
                                   DJANGO_SECRET_KEY=... \
                                   DATABASE_URL=postgres://municipal_finance:...@postgresq....amazonaws.com/municipal_finance
```


## Running dabatase migrations in production

When it makes sense to deploy first, then run migrations, it's best to do so in a linux `screen` or whatever remote shell you prefer to avoid losing your connection while it's running.

```
ssh ubuntu@municipalmoney.gov.za
dokku run municipal-finance bash
PRELOAD_CUBES=false python manage.py migrate
```
If your migrations take more than 30s and you're not affecting masses of users during popular hours, you can extend the transaction timeout like so
```
DB_STMT_TIMEOUT=30000000 PRELOAD_CUBES=false python manage.py migrate
```

# Initial Data Import

Data import is still a fairly manual process leveraging the DB and a few SQL scripts to do the hard work. This is usually done against a local DB, sanity checked with a locally-running instance of the API and some tools built on it, and if everything looks ok, dumped table-by-table with something like `pg_dump "postgres://municipal_finance@localhost/municipal_finance" --table=audit_opinions -O -c --if-exists > audit_opinions.sql` and then loaded into the production database.

1. `python manage.py migrate`
2. Create the tables with `cat sql/create/* | psql municipal_finance`
3. Import the first few columns of the fact tables which are supplied by National Treasury
 - e.g. `psql# \copy incexp(demarcation_code, period_code, function_code, item_code, amount) FROM '/bob/incexp_2015q4.csv' DELIMITER ',' CSV HEADER`
4. Run `sql/decode_period_code.sql` to populate the remaining columns from the period code
  - These should be idempotent so they can simply run again when data is added.
5. Import the dimension table data from `municipal_finance/data_import/dimension_tables`
6. Make sure `create_indices.sql` and its indices are up to date
  - create it with the python module `municiapl_finance.data_import.create_indices`
  - add it to git and run it if it was changed
  - the prod DB doesn't support CREATE INDEX IF NOT EXISTS yet so ignore errors for existing indices unless their columns changed and they need to be manually removed and recreated.

*Remember to run `VACUUM ANALYSE` or REINDEX tables after significant changes to ensure stats are up to date to use indices properly.*


# Capital Projects


## Loading new capital projects
`python manage.py load_infrastructure_projects <municode> <filename>`

- <municode> is should be one of the official municipal codes such as CPT, WC011, KZN121, etc
- <filename> is a csv file with the following headings
"Function","Project Description","Project Number","Type","MTSF Service Outcome","IUDF","Own Strategic Objectives","Asset Class","Asset Sub-Class","Ward Location","GPS Longitude","GPS Latitude","Audited Outcome 2017/18","Full Year Forecast 2018/19","Budget year 2019/20","Budget year 2020/21","Budget year 2021/22"


## TODO
Currently the following columns are expected in the capital projects input files:

- Audited Outcome 2017/18
- Full Year Forecast 2018/19
- Budget year 2019/20
- Budget year 2020/21
- Budget year 2021/22

This will need to change once the file format is finalised


# Standard Operating Procedure

This covers how to keep the data up to date. Each quarter, as new data is released, the following needs to be done to update the data served by the API and the Citizen Scorecard. It's best to do this on a test database first and validate the results before updating the production database.

 - Quarter 1
   - Contacts
   - Latest monthly actuals
   - Corrections all over
 - Quarter 2
   - Contacts
   - Latest monthly actuals
   - Corrections all over
   - **Audited Annual data from last financial year**
 - Quarter 3
   - Contacts
   - Latest monthly actuals
   - Corrections all over
   - **Audit outcomes for last financial year**
   - **Unauthorised, Irregular, and Fruitless and Wasteful expenditure from financial year before last**
 - Quarter 4
   - Contacts
   - Latest monthly actuals
   - Corrections all over

## Extract CSV datasets from Excel Spreadsheets

Install some additional dependencies:
- `source env/bin/activate`
- `pip install bs4` - bs4 is used to scrape audit report URLs
- `pip install csvkit` - optional - convenient tools for inspecting and querying CSVs

Extract CSV datasets from Excel Spreadsheets using the following scripts in `municipal_finance/data_import/`

- audit_opinions.py
  - Budget Document Tracking - Reporting > List Audit Opinion
  - Location Level: Municipality
  - Financial Year End(s): Control+Click the four years up to and including the last audit result available
  - Sort Options: By Municipality
  - Choose Excel 2000 report format
  - Process Request: The downloaded file has .xls extension but is html - open in libreoffice or excel and save explicitly as .xls again.
- contact_details.py
  - Go to the [local government database](https://lg.treasury.gov.za/iworld/default_prov.htm)
  - Contacts - Reporting > General Information - Municipalities Individuals
  - Choose Municipal level
  - Choose relevant roles
  - Choose Excel 2000 report format
  - Download report, open in excel, save as xlsx (the website gives HTML in .xls)
  - Process Request: The downloaded file has .xls extension but is html - open in libreoffice or excel and save explicitly as .xls again.
- uifw_expenditure.py
  - input files like [01. Irregular Expenditures - Master 04 December 2014](http://mfma.treasury.gov.za/Media_Releases/mbi/2014/Documents/G.%20Additional%20information)


## Scrape the MFMA website for the Audit Report URLs into a CSV file

Using `municipal_finance/data_import/audit_reports.py`


## Insert/update from CSV files

1. Update the paths in the per-cube files in `sql/upsert/`
2. Execute the files
  - This takes about 30 minutes for incexp, a bit less for capital, and the rest are much quicker.

These files work as follows:

1. Create a temporary table
2. Import the CSV file to the temporary table
4. Delete all rows for which a matching demarcation code and period code occurs in the update dataset
  - e.g. if BUF 2016AUDA is in the update, all BUF 2016AUDA rows will be deleted from the update dataset. That means line items that were removed from the Treasury Local Government Database and aren't in quarterly update datasets will also be removed from the Municipal Data database.
  - if a demarcation code and period code is already in the database and not in the update dataset, it will remain in the Municipal Data database.
5. Insert all rows of the update dataset to the fact table
  - `period_code` is decoded into `financial_period`, `financial_year`, `amount_type` on the fly. Unexpected values result in SQL errors, aborting the transaction.

Update the last-updated date in the model files for each cube in `models/*.json`

Update the materialised view data using `bin/materialised_views.py`:

You might need to allow extra open files with something like `ulimit -n 500000`

1. Run with --profiles-from-api to update the muni-specific profile data
 - This takes about 6 minutes locally
2. Run with --calc-medians and --calc-rating-counts to update comparison data based on profile changes.
3. Check what changed using `git diff` and commit commit if changes look right.
4. Run `bin/test-pages.sh` and ensure that all pages return "200 OK"


## Annual data

Whenever Audited Annual data becomes available (AUDA financial data and Audit Outcomes), adjust the years used by `scorecard/profile_data.py` to include the latest financial year available.

Audit outcomes will be captured in the months following 1 December following the end of the financial year. Audited figures can start being submitted by municipalities to Treasury from this point. That means new audited annual figures can appear from Q2.

Pre-audit figures are captured in the period 3 Aug to 30 Nov after the end of the financial year.


## Quarterly data

Indicators using quarterly data automatically use the latest quarter available.

Quarterly Section 71 submissions are available 2 months after the end of the quarter.


## Validating the data

The aim here is to ensure that the data is in the correct format, and that the import worked correctly, such that the correct values are shown to users of the site. That means the right number is returned, for a given line item, for a given period and municipality. The correct number is defined by what has been provided in the snapshot from Treasury. This can be sanity-checked by comparing to what's published on the MFMA website. Examples of the kind of errors this is trying to catch are:

- different number formats
- different line item codes
- different data structures which aren't detected by the database constraints, but can be detected by manually comparing the numbers presented to published documents

This shouldn't be exhaustive - when some numbers in each dataset match expected values, we can infer that the data is imported correctly. The strategy is to identify a few changes between subsequent snapshots, and check that they are reflected in the API. Since distinctions aren't made between importing different municipalities, other municipalities should be imported equivalently.

Check that the column order in the snapshots match those in the _"upsert"_ scripts. e.g.:

```shell
head -1 2017q2/*
```

Quickly get an idea of what was updated in the datasets: compare this snapshot to the previous for each dataset:

e.g. with the command `diff <(sort ../../2016q4/Section\ 71\ Q4\ published\ data/bsheet_2016q4_acrmun.csv) <(sort bsheet_2017q1_acrmun.csv)|less`
Search for `<` to find a row that was removed, paging past the period codes that fell out of the update window to some lines where one value was swapped for another. This example shows a value that was swapped from one item code to another, and a second change where a number changed by R1. Check that this change is correctly reflected in the API using the API itself or the table view where possible.
```
3951c1901
< "DC12","2015AUDA","1400",128859696.00
---
> "DC12","2015AUDA","1400",1000.00
3958c1908
< "DC12","2015AUDA","1500",1000.00
---
> "DC12","2015AUDA","1500",128859696.00
3960c1910
< "DC12","2015AUDA","1650",4952698143.00
---
> "DC12","2015AUDA","1650",4952698144.00
```

Do each of these cursory tests for a small sample of municipalities to sanity-check. Focus on things you know have changed.

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
  - Use the _consolidated_ financial statements where available for municipalities with multiple entities
  - You can compare some values in the Scorecard site and the rest in the Table View
  - Debtor (under Consumer Receivables) and Creditor age analysis can be found in the AFS
  - Make sure to check unauthorised, irregular, fruitless and wasteful expenditure
- Compare in-year values to [Section 71 in-year reports](http://mfma.treasury.gov.za/Media_Releases/s71/Pages/default.aspx)
  - Use the API or the database for datasets not available in the Table View:
    - e.g. `select l.label, l30_amount from aged_debtor_facts f, aged_debtor_items l where f.item_code = l.code and demarcation_code = 'CPT' and financial_year = 2016 and financial_period = 09 and amount_type_code = 'ACT';`
  - Compare the latest available month of a quarter to the quarter value in the report


# Upsert Log


## 2016q4

- Some of the files had amounts ending .00 so to check that simply rounding was ok, I ran `grep -v  '\.00' *|egrep  -v "(capital|cflow|grants|rm_)"` - the excluded files didn't have .00 endings.


## 2017q4

- cflow monthly amounts doubled from previous snapshots where they occurred. It turned out this was due to an issue in the query used to generate the snapshot and a new cflow snapshot was supplied.


## 2018q1

- capital and creditor age had unexpected codes for one KZN muni. Marina said we should filter them out.


## 2018q3

- The audit opinion label `Unqualified - With findings` should get mapped to `Unqualified - Emphasis of Matter items` - confirmed with Elsabe.


## 2019-07-09 loading Section 71 Q3 2018-19

e.g. `cat sql/upsert/aged_debtor.sql | docker-compose run --rm postgres psql postgresql://postgres@postgres/municipal_finance`


# License

MIT License
