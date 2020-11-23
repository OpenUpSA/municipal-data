
import tablib

from django.db import migrations


def run_data_import(resource, filename):

    def import_initial_data(apps, schema_editor):
        dataset = tablib.Dataset().load(
            open(f'municipal_finance/fixtures/initial/{filename}'),
            format='csv',
            headers=True,
        )
        resource().import_data(dataset, raise_errors=True)

    return migrations.RunPython(import_initial_data)
