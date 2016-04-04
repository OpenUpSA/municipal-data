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