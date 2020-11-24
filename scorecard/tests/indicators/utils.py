import tablib

from functools import wraps
from concurrent.futures import ThreadPoolExecutor

from django.db import connections, DEFAULT_DB_ALIAS
from django.test import TransactionTestCase, override_settings

from municipal_finance.cubes import get_manager

from ...profile_data import ApiClient


def import_data(resource, filename):
    resource().import_data(
        tablib.Dataset().load(
            open(f'scorecard/fixtures/tests/indicators/{filename}'),
            format='csv',
            headers=True,
        ),
        raise_errors=True,
    )


class DjangoConnectionThreadPoolExecutor(ThreadPoolExecutor):
    """
    When a function is passed into the ThreadPoolExecutor via either submit() or map(), 
    this will wrap the function, and make sure that close_django_db_connection() is called 
    inside the thread when it's finished so Django doesn't leak DB connections.

    Since map() calls submit(), only submit() needs to be overwritten.
    """

    def close_django_db_connection(self):
        connections[DEFAULT_DB_ALIAS].close()

    def generate_thread_closing_wrapper(self, fn):
        @wraps(fn)
        def new_func(*args, **kwargs):
            try:
                res = fn(*args, **kwargs)
            except Exception as e:
                self.close_django_db_connection()
                raise e
            else:
                self.close_django_db_connection()
                return res
        return new_func

    def submit(*args, **kwargs):
        """
        I took the args filtering/unpacking logic from 

        https://github.com/python/cpython/blob/3.7/Lib/concurrent/futures/thread.py 

        so I can properly get the function object the same way it was done there.
        """
        if len(args) >= 2:
            self, fn, *args = args
            fn = self.generate_thread_closing_wrapper(fn=fn)
        elif not args:
            raise TypeError("descriptor 'submit' of 'ThreadPoolExecutor' object "
                            "needs an argument")
        elif 'fn' in kwargs:
            fn = self.generate_thread_closing_wrapper(fn=kwargs.pop('fn'))
            self, *args = args

        return super(self.__class__, self).submit(fn, *args, **kwargs)


@override_settings(
    SITE_ID=3,
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
)
class IndicatorTestCase(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        # Setup the API client
        self.executor = DjangoConnectionThreadPoolExecutor(max_workers=1)
        self.api_client = ApiClient(
            lambda u, p: self.executor.submit(self.client.get, u, data=p),
            "/api"
        )

    def tearDown(self):
        get_manager().engine.dispose()
