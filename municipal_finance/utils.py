from datetime import date
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


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
