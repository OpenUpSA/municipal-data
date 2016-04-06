from datetime import date
from decimal import Decimal

from werkzeug.exceptions import NotFound

# from babbage.exc import BabbageException

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from cubes import cube_manager


def get_cube(name):
    """ Load the named cube from the current registered ``CubeManager``. """
    if not cube_manager.has_cube(name):
        # TODO: check this
        raise NotFound('No such cube: %r' % name)
    return cube_manager.get_cube(name)


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


# @blueprint.errorhandler(BabbageException)
def handle_error(exc):
    return jsonify({
        'status': 'error',
        'message': exc.message,
        'context': exc.context
    }, status=exc.http_equiv)


# @blueprint.route('/')
def index(request):
    """ General system status report :) """
    from babbage import __version__, __doc__
    return jsonify({
        'status': 'ok',
        'api': 'babbage',
        'message': __doc__,
        'version': __version__
    })


# @blueprint.route('/cubes')
def cubes(request):
    """ Get a listing of all publicly available cubes. """
    cubes = []
    for cube in cube_manager.list_cubes():
        cubes.append({
            'name': cube
        })
    return jsonify({
        'status': 'ok',
        'data': cubes
    })


# @blueprint.route('/cubes/<name>/model')
def model(request, cube_name):
    """ Get the model for the specified cube. """
    cube = get_cube(cube_name)
    return jsonify({
        'status': 'ok',
        'name': cube_name,
        'model': cube.model
    })


def aggregate(request, cube_name):
    """ Perform an aggregation request. """
    cube = get_cube(cube_name)
    result = cube.aggregate(aggregates=request.GET.get('aggregates'),
                            drilldowns=request.GET.get('drilldown'),
                            cuts=request.GET.get('cut'),
                            order=request.GET.get('order'),
                            page=request.GET.get('page'),
                            page_size=request.GET.get('pagesize'))
    result['status'] = 'ok'
    return jsonify(result)


def facts(request, cube_name):
    """ List the fact table entries in the current cube. This is the full
    materialized dataset. """
    cube = get_cube(cube_name)
    result = cube.facts(fields=request.GET.get('fields'),
                        cuts=request.GET.get('cut'),
                        order=request.GET.get('order'),
                        page=request.GET.get('page'),
                        page_size=request.GET.get('pagesize'))
    result['status'] = 'ok'
    return jsonify(result)


def members(request, cube_name, member_ref):
    """ List the members of a specific dimension or the distinct values of a
    given attribute. """
    cube = get_cube(cube_name)
    result = cube.members(member_ref,
                          cuts=request.GET.get('cut'),
                          order=request.GET.get('order'),
                          page=request.GET.get('page'),
                          page_size=request.GET.get('pagesize'))
    result['status'] = 'ok'
    return jsonify(result)
