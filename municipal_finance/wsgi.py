"""
WSGI config for code4sa project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "municipal_finance.settings")

# patch psycopg2 to use asyncio with gevent
# see https://pypi.python.org/pypi/psycogreen/1.0
from psycogreen.gevent import patch_psycopg
patch_psycopg()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
