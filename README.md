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

1. Create the table with the file in the `sql` dir with the table's name, e.g.
2. Import the first few columns which are supplied by National Treasury
3. Run the relevant add_labels_-prefixed SQL file to add the remaining labels.
  - These should be idempotent so they can simply run again when data is added.

*Remember to run `VACUUM ANALYSE` aftersignificant changes to ensure stats are up to date to use indices properly.*

# License

MIT License
