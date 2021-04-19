# Municipal Money

Municipal Money is a project between the [South African National Treasury](http://www.treasury.gov.za/) and [OpenUp](https://openup.org.za) to
make municipal finance information available to the public. It is made up of a citizen-facing app and an API.

In production, the two sites are served by one Django instance, using the hostname to determine which site to serve. In development, we use the SITE_ID environment variable to select the site, and run two instances when needed:

| Site                                 | Production URL                         | docker-compose service name | Django Sites ID |
|--------------------------------------|----------------------------------------|-----------------------------|-----------------|
| Public-friendly site                 | https://municipalmoney.gov.za/         | scorecard                   | 2               |
| Data exploration/download UI and API | https://municipaldata.treasury.gov.za/ | portal                      | 3               |


## Local development setup


### Scorecard website

If you only want to work on the Scorecard website you can run it with a small sample of
[demo data](#demo-data) to be able to see the scorecard features without loading a full
database dump. The site will use pre-calculated
financials and link to the production data/API site for detail.

In one terminal, run

```
docker-compose run --rm scorecard yarn dev
```

```
docker-compose up -d postgres
docker-compose run --rm scorecard python manage.py migrate
docker-compose run --rm scorecard python manage.py loaddata demo-data seed-data
docker-compose up scorecard
```

If you are working on the javascript or CSS on the site also run `yarn dev` in another terminal.

To create an admin user for local development, run

```
docker-compose run --rm scorecard python manage.py createsuperuser
```


### Data portal website

If you want to run the API and data portal locally using `docker-compose` you also need to:

1. Dump the production database.
2. Load the production database dump into your `docker-compose` postgres instance
   (this will take at least 40 minutes) with something like:

```
docker-compose run --rm -v /home/user/folder-containing-dumpdata/:/data \
   portal pg_restore -h postgres -U municipal_finance -d municipal_finance /data/dumpfile
```

3. Run the data portal:

```
docker-compose up portal
```


### Demo data

A small number of municipalities are used for demo data. They are selected to satisfy
the following needs:

- minimal data to minimise effort in checking changes to the demo data
- a metros to demonstrate metro-only functionality
- a district to demonstrate navigation to local municipalities via districts on the map
- a local municipality
- at least two examples of each in different provinces to demonstrate comparison to similar municipalities

The following municipalities are available in the demo data:

```
TSH, BUF, GT483, GT481, EC109, EC108, DC48, DC12, DC10, 
```

#### Maintaining demo data

Ensure you only have the demo data municipalities and only their data in the database.

You need fiscal data loaded for at least the demo municipalities to be able to rebuild their profiles.

Run a profile rebuild.

Run

```
docker-compose run --rm scorecard python manage.py dumpdata --indent 2 \
    scorecard.geography \
    municipal_finance.municipalityprofile \
    municipal_finance.mediangroup \
    municipal_finance.ratingcountgroup \
    > demo-data.json
```

Run git diff and check that the diff looks sensible - that you're only adding/modifying
what you intend to.

Commit the changes to git.


### Importing Webflow exports

1. Ensure that you have Node.JS installed. (tested with version `14.15.4`)
2. Run the `import-webflow-export` command, providing the path to the export file:

```
npx import-webflow-export /path/to/webflow-export.zip
```

Read more about the decision to use Webflow and best practices for using it here:
- https://app.gitbook.com/@openup/s/handbook/how-we-work/organisational-decision-records/odr2-building-dynamic-web-frontends-using-webflow
- https://app.gitbook.com/@openup/s/handbook/tech/webflow-best-practice/custom-dom-manipulation-in-webflow-sites


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
