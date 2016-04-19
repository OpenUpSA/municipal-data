from datetime import date, datetime
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.http import StreamingHttpResponse
from django.http import JsonResponse

import csv


class BabbageJSONEncoder(DjangoJSONEncoder):
    """ Custom JSONificaton to support obj.to_dict protocol. """
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, set):
            return [o for o in obj]
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return super(BabbageJSONEncoder, self).default(obj)


def jsonify(obj, status=200, headers=None):
    return JsonResponse(obj, BabbageJSONEncoder, safe=False)


class EchoBuffer(object):
    """An object that implements just the write method of the file-like
    interface.
    https://docs.djangoproject.com/en/1.9/howto/outputting-csv/#streaming-large-csv-files
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def csvify(name_base, fields, rows):
    header_row = {}
    for field in fields:
        header_row[field] = field
    rows = [header_row] + rows

    writer = csv.DictWriter(EchoBuffer(), fields)
    stream = (writer.writerow(row) for row in rows)
    response = StreamingHttpResponse(stream, content_type='text/csv')
    filename = name_base + '_' + datetime.now().isoformat() + '.csv'
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response
