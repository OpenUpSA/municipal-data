for cube in `curl  http://localhost:8000/api/cubes|jq -r .data[].name`
do
    TABLE=`curl http://localhost:8000/api/cubes/$cube/model|jq -r '.model.fact_table'`
    for dimension in `curl http://localhost:8000/api/cubes/$cube/model|jq -r '.model.dimensions|keys[]'`
    do
        for attribute in `curl http://localhost:8000/api/cubes/$cube/model|jq -r ".model.dimensions.$dimension.attributes|keys[]"`
        do
            COL=`curl http://localhost:8000/api/cubes/$cube/model|jq -r ".model.dimensions.$dimension.attributes.$attribute.column"`
            echo "create index if not exists ${TABLE}_${COL}_idx on $TABLE ($COL);"
        done
    done
done
