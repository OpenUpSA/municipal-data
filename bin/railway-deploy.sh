#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python manage.py collectstatic --noinput
export PRELOAD_CUBES=false
python manage.py migrate --no-input
export PRELOAD_CUBES=true
gunicorn  --limit-request-line 8190 --worker-class gevent municipal_finance.wsgi:application --log-file - --bind 0.0.0.0:${PORT:-5000} --timeout 480
