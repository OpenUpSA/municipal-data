for muni in `curl 'http://localhost:8001/api/cubes/municipalities/members/municipality.demarcation_code?format=csv'|dos2unix|grep -v municipality.demarcation_code`
do
    if [[ ${muni} == DC* ]]
    then
        prefix=district-${muni}
    else
        prefix=municipality-${muni}
    fi
    curl -o /dev/null -vL http://localhost:8000/profiles/${prefix}/ 2>&1 | grep HTTP/1 | grep -v 301
done
