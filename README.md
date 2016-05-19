# municpal data

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

# Data Import

Data import is still a fairly manual process leveraging the DB and a few SQL scripts to do the hard work. This is usually done against a local DB, sanity checked with a locally-running instance of the API and some tools built on it, and if everything looks ok, dumped table-by-table with something like `pg_dump "postgres://municipal_finance@localhost/municipal_finance" --table=audit_opinions -O -c --if-exists > audit_opinions.sql` and then loaded into the production database.

1. Create the tables with the `table_`-prefixes SQL files in the `sql` dir.
2. Import the first few columns of the fact tables which are supplied by National Treasury
 - e.g. `psql# \copy incexp(demarcation_code, period_code, function_code, item_code, amount) FROM '/bob/incexp_2015q4.csv' DELIMITER ',' CSV HEADER`
3. Run `sql/decode_period_code.sql` to populate the remaining columns from the period code
  - These should be idempotent so they can simply run again when data is added.
4. Import the dimension table data from `municipal_finance/data_import/dimension_tables`
5. Make sure `create_indices.sql` and its indices are up to date
  - create it with the python module `municiapl_finance.data_import.create_indices`
  - add it to git and run it if it was changed
  - the prod DB doesn't support CREATE INDEX IF NOT EXISTS yet so ignore errors for existing indices unless their columns changed and they need to be manually removed and recreated.

*Remember to run `VACUUM ANALYSE` or REINDEX tables after significant changes to ensure stats are up to date to use indices properly.*

# License

MIT License
