# municpal data api

## run

    source env/bin/activate
    python api.py

## query

See also [Babbage HTTP API](https://github.com/openspending/babbage#using-the-http-api)

### All itmes

    curl  localhost:5000/api/cubes/incexp/facts|jq .


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

    curl  'localhost:5000/api/cubes/incexp/facts?cut=incexp_code.incexp_code:"6600"%7Cperiod.period:"2016ORGB"%7Cfunction.function_code:"903"'|jq .

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

    curl  localhost:5000/api/cubes/incexp/members/incexp_code|jq .

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