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

# Examples

## UI

http://localhost:8000/#/?fields=amount&fields=function.function_desc&fields=incexp_code.incexp_desc&fields=period.period&fields=demarcation_code.demarcation_code&order=amount:desc

## API queries

See also [Babbage HTTP API](https://github.com/openspending/babbage#using-the-http-api)

### All itmes

    curl  localhost:8000/cubes/incexp/facts|jq .


```json
...
    {
      "demarcation_code.demarcation": "CPT",
      "incexp_code.incexp_code": "6230",
      "incexp_code.incexp_desc": "Depreciation Reserve Ex Afr",
      "period.period": "2016IBY2",
      "function.function_code": "1001",
      "amount": 12829478,
      "function.function_desc": "Waste Water Management/Sewerage"
    },
...
```

### Filtered items

    curl  'localhost:8000/cubes/incexp/facts?cut=incexp_code.incexp_code:"6600"%7Cperiod.period:"2016ORGB"%7Cfunction.function_code:"903"'|jq .

```json
{
  "status": "ok",
  "total_fact_count": 4,
  "fields": [
    "function.function_code",
    "function.function_desc",
    "incexp_code.incexp_code",
    "incexp_code.incexp_desc",
    "period.period",
    "demarcation_code.demarcation_code",
    "amount"
  ],
  "page_size": 10000,
  "page": 1,
  "cell": [
    {
      "operator": ":",
      "ref": "incexp_code.incexp_code",
      "value": "6600"
    },
    {
      "operator": ":",
      "ref": "period.period",
      "value": "2016ORGB"
    },
    {
      "operator": ":",
      "ref": "function.function_code",
      "value": "903"
    }
  ],
  "data": [
    {
      "incexp_code.incexp_code": "6600",
      "incexp_code.incexp_desc": "Plus Interests In Entities Not Wholly Owned",
      "period.period": "2016ORGB",
      "function.function_code": "903",
      "amount": null,
      "function.function_desc": "Environmental Protection/Other",
      "demarcation_code.demarcation_code": "BUF"
    },
    {
      "incexp_code.incexp_code": "6600",
      "incexp_code.incexp_desc": "Plus Interests In Entities Not Wholly Owned",
      "period.period": "2016ORGB",
      "function.function_code": "903",
      "amount": null,
      "function.function_desc": "Environmental Protection/Other",
      "demarcation_code.demarcation_code": "MAN"
    },
    {
      "incexp_code.incexp_code": "6600",
      "incexp_code.incexp_desc": "Plus Interests In Entities Not Wholly Owned",
      "period.period": "2016ORGB",
      "function.function_code": "903",
      "amount": null,
      "function.function_desc": "Environmental Protection/Other",
      "demarcation_code.demarcation_code": "NMA"
    },
    {
      "incexp_code.incexp_code": "6600",
      "incexp_code.incexp_desc": "Plus Interests In Entities Not Wholly Owned",
      "period.period": "2016ORGB",
      "function.function_code": "903",
      "amount": null,
      "function.function_desc": "Environmental Protection/Other",
      "demarcation_code.demarcation_code": "TSH"
    }
  ],
  "order": []
}
```

### Income/Expenditure codes and their labels

    curl  localhost:8000/cubes/incexp/members/incexp_code|jq .

```json
{
  "status": "ok",
  "fields": [
    "incexp_code.incexp_code",
    "incexp_code.incexp_desc"
  ],
  "page_size": 10000,
  "order": [],
  "cell": [],
  "total_member_count": 61,
  "data": [
    {
      "incexp_code.incexp_code": "1000",
      "incexp_code.incexp_desc": "Interest Earned - Outstanding Debtors"
    },
    {
      "incexp_code.incexp_code": "1100",
      "incexp_code.incexp_desc": "Dividends Received"
    },
    {
      "incexp_code.incexp_code": "1300",
      "incexp_code.incexp_desc": "Fines"
    },
```

# License

MIT License
