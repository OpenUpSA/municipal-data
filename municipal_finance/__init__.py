from django.apps import AppConfig

default_app_config = 'municipal_finance.Config'


class Config(AppConfig):
    name = 'municipal_finance'
    verbose_name = 'Municipal Finance API'

    def ready(self):
        # Unused import to initialise cube_manager
        import cubes
