
import tablib


def import_data(resource, filename):
    resource().import_data(
        tablib.Dataset().load(
            open(f'scorecard/fixtures/tests/{filename}').read(),
            format='csv',
            headers=True,
        ),
        raise_errors=True,
    )

