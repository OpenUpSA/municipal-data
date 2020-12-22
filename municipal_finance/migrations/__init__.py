
import tablib

from django.db import migrations

from ..utils import import_data


def run_data_import(resource, filename):

    def import_initial_data(apps, schema_editor):
        import_data(resource, f'municipal_finance/fixtures/initial/{filename}')

    return migrations.RunPython(import_initial_data)
