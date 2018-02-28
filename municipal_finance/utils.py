from datetime import date, datetime
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.http import StreamingHttpResponse, Http404, HttpResponse
from django.http import JsonResponse
from io import BytesIO

import xlsxwriter
import unicodecsv as csv


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
    return JsonResponse(obj, BabbageJSONEncoder, safe=False, status=status)


class EchoBuffer(object):
    """An object that implements just the write method of the file-like
    interface.
    https://docs.djangoproject.com/en/1.9/howto/outputting-csv/#streaming-large-csv-files
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def csvify(fields, rows):
    header_row = {}
    for field in fields:
        header_row[field] = field
    rows = [header_row] + rows

    writer = csv.DictWriter(EchoBuffer(), fields)
    stream = (writer.writerow(row) for row in rows)
    return StreamingHttpResponse(stream, content_type='text/csv')


def xlsxify(fields, rows):
    output = BytesIO()
    wb = xlsxwriter.Workbook(output)
    ws = wb.add_worksheet('data')

    data = [[r[f] for f in fields] for r in rows]

    ws.add_table(0, 0, len(rows), len(fields) - 1, {
        'columns': [{'header': f} for f in fields],
        'data': data,
    })

    wb.close()
    output.seek(0)
    output = output.read()

    return HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


def serialize(format, name_base, fields, rows):
    if format == 'csv':
        response = csvify(fields, rows)
    elif format == 'xlsx':
        response = xlsxify(fields, rows)
    else:
        raise Http404()

    filename = name_base + '_' + datetime.now().isoformat() + '.%s' % format
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response


def check_page_size(page_size):
    return int(page_size) or 10000
