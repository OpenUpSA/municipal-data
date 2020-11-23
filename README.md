# Municipal Money

Municipal Money is a project between the [South African National Treasury](http://www.treasury.gov.za/) and [OpenUp](https://openup.org.za) to
make municipal finance information available to the public. It is made up of a citizen-facing app and an API.

In production, the two sites are served by one Django instance, using the hostname to determine which site to serve. In development, we use the SITE_ID environment variable to select the site, and run two instances when needed:

| Site                                 | Production URL                         | docker-compose service name | Django Sites ID |
|--------------------------------------|----------------------------------------|-----------------------------|-----------------|
| Public-friendly site                 | https://municipalmoney.gov.za/         | scorecard                   | 2               |
| Data exploration/download UI and API | https://municipaldata.treasury.gov.za/ | portal                      | 3               |

## Local development quick start (with docker-compose)

If you only want to work on the Scorecard website. The site will use pre-calculated
financials and link to the production data/API site for detail.

In one terminal, run

```
docker-compose run --rm scorecard yarn dev
```

```
docker-compose up -d postgres
docker-compose run --rm scorecard python manage.py migrate
docker-compose run --rm scorecard python manage.py loaddata demo-data
docker-compose up scorecard
```

If you want to run the API and data portal locally using docker-compose you also need to:


1. Dump the production database.
2. Load the production database dump into your docker-compose postgres instance
   (this will take at least 40 minutes) with something like:

```
docker-compose -f docker-compose.yml -f docker-compose.portal.yml \
               run --rm -v /home/user/folder-containing-dumpdata/:/data \
               portal pg_restore -h postgres -U municipal_finance -d municipal_finance /data/dumpfile
```

3. Run the API and data portal along with the scorecard site with something like:

```
docker-compose -f docker-compose.yml -f docker-compose.portal.yml up portal scorecard
```


### Updating municipality profile data in Docker

Run the portal service using `gunicorn` instead of django's `runserver`:

```
docker-compose -f docker-compose.yml -f docker-compose.portal.yml -f docker-compose.portal-gunicorn.yml up portal
```

Run the update scripts against the portal service:

```
docker-compose -f docker-compose.yml run --rm scorecard python bin/materialised_views.py --api-url http://portal:8000/api --profiles-from-api
```

Any changes should be written to the JSON files in the container, which are mapped into the container from the repository directory.


## Local development (without docker)

1. Clone this repo
2. Create a Python virtual environment. ```virtualenv <env_name>```
3. Activate virtual environment ``` source <env_name>/bin/activate```
4. Install dependencies:

   Some python packages require system packages.
   * psycopg2 requires libpq-dev (postgresql development files).
   * gnureadline requires libncurses5-dev (ncurses development files).
   * multiple packages require python development files (python-dev).

   After these packages have being installed the python packages can then be installed. ```pip install -r requiments.txt```

5. Install `postgresql` and create a user and a database.

   ``createuser municipal_finance -W``

   * -W will prompt to create a password for the user.

   ``createdb municipal_finance -O municipal_finance``

   * -O will give ownership of the database to the `municipal_finance` user.

6. Install data from somewhere :)

7. Run it: ``python manage.py runserver``

Note when doing a high request rate locally e.g. during updates, it seems that the above command doesn't release resources quickly enough so use the following for the API server instead:

```bash
export DJANGO_SETTINGS_MODULE=municipal_finance.settings
export API_URL=http://localhost:8001/api  # only needed if using the table view against local API
export PRELOAD_CUBES=true
export SITE_ID=3
gunicorn --limit-request-line 7168 --worker-class gevent municipal_finance.wsgi:application -t 600 --log-file -
```


## Production

```
dokku config:set municipal-finance DJANGO_DEBUG=False \
                                   DISABLE_COLLECTSTATIC=1 \
                                   DJANGO_SECRET_KEY=... \
                                   DATABASE_URL=postgres://municipal_finance:...@postgresq....amazonaws.com/municipal_finance
```


### Running database migrations in production

When it makes sense to deploy first, and only then run migrations, it's best to do so in a linux `screen` or whatever remote shell you prefer to avoid losing your connection while it's running.

```
ssh ubuntu@municipalmoney.gov.za
dokku run municipal-finance bash
PRELOAD_CUBES=false python manage.py migrate
```

If your migrations take more than 30s and you're not affecting masses of users during popular hours, you can extend the transaction timeout like so:

```
DB_STMT_TIMEOUT=30000000 PRELOAD_CUBES=false python manage.py migrate
```

## Initial Data Import

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


## Capital Projects


### Loading new capital projects

`python manage.py load_infrastructure_projects <municode> <filename>`

- <municode> is should be one of the official municipal codes such as CPT, WC011, KZN121, etc
- <filename> is a csv file with the following headings
"Function","Project Description","Project Number","Type","MTSF Service Outcome","IUDF","Own Strategic Objectives","Asset Class","Asset Sub-Class","Ward Location","GPS Longitude","GPS Latitude","Audited Outcome 2017/18","Full Year Forecast 2018/19","Budget year 2019/20","Budget year 2020/21","Budget year 2021/22"

### TODO

Currently the following columns are expected in the capital projects input files:

- Audited Outcome 2017/18
- Full Year Forecast 2018/19
- Budget year 2019/20
- Budget year 2020/21
- Budget year 2021/22

This will need to change once the file format is finalised


## License

MIT License
