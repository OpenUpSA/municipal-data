from django.apps import AppConfig
import settings
from cubes import get_manager

default_app_config = 'municipal_finance.Config'


class Config(AppConfig):
    name = 'municipal_finance'
    verbose_name = 'Municipal Finance API'

    def ready(self):
        if settings.PRELOAD_CUBES:
            # Running a server
            get_manager()
