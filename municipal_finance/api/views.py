from datetime import date
from decimal import Decimal

from werkzeug.exceptions import NotFound

from babbage.exc import BabbageException

from django.http import JsonResponse


def get_manager():
    """ Try to locate a ``CubeManager`` on the Flask app which is currently
    processing a request. This will only work inside the request cycle. """
    return current_app.extensions['babbage']


def get_cube(name):
    """ Load the named cube from the current registered ``CubeManager``. """
    manager = get_manager()
    if not manager.has_cube(name):
        raise NotFound('No such cube: %r' % name)
    return manager.get_cube(name)


# class JSONEncoder(json.JSONEncoder):
#     """ This encoder will serialize all entities that have a to_dict
#     method by calling that method and serializing the result. """
#
#     def default(self, obj):
#         if isinstance(obj, date):
#             return obj.isoformat()
#         if isinstance(obj, Decimal):
#             return float(obj)
#         if isinstance(obj, set):
#             return [o for o in obj]
#         if hasattr(obj, 'to_dict'):
#             return obj.to_dict()
#         return json.JSONEncoder.default(self, obj)

def jsonify(obj, status=200, headers=None):
    """ Custom JSONificaton to support obj.to_dict protocol. """
    data = obj
    return JsonResponse(data, headers=headers, status=status)




# @blueprint.errorhandler(BabbageException)
def handle_error(exc):
    return jsonify({
        'status': 'error',
        'message': exc.message,
        'context': exc.context
    }, status=exc.http_equiv)


# @blueprint.route('/')
def index():
    """ General system status report :) """
    from babbage import __version__, __doc__
    return jsonify({
        'status': 'ok',
        'api': 'babbage',
        'message': __doc__,
        'version': __version__
    })


# @blueprint.route('/cubes')
def cubes():
    """ Get a listing of all publicly available cubes. """
    cubes = []
    for cube in get_manager().list_cubes():
        cubes.append({
            'name': cube
        })
    return jsonify({
        'status': 'ok',
        'data': cubes
    })


# @blueprint.route('/cubes/<name>/model')
def model(name):
    """ Get the model for the specified cube. """
    cube = get_cube(name)
    return jsonify({
        'status': 'ok',
        'name': name,
        'model': cube.model
    })


# @blueprint.route('/cubes/<name>/aggregate')
def aggregate(name):
    """ Perform an aggregation request. """
    cube = get_cube(name)
    result = cube.aggregate(aggregates=request.args.get('aggregates'),
                            drilldowns=request.args.get('drilldown'),
                            cuts=request.args.get('cut'),
                            order=request.args.get('order'),
                            page=request.args.get('page'),
                            page_size=request.args.get('pagesize'))
    result['status'] = 'ok'
    return jsonify(result)


# @blueprint.route('/cubes/<name>/facts')
def facts(name):
    """ List the fact table entries in the current cube. This is the full
    materialized dataset. """
    cube = get_cube(name)
    result = cube.facts(fields=request.args.get('fields'),
                        cuts=request.args.get('cut'),
                        order=request.args.get('order'),
                        page=request.args.get('page'),
                        page_size=request.args.get('pagesize'))
    result['status'] = 'ok'
    return jsonify(result)


# @blueprint.route('/cubes/<name>/members/<ref>')
def members(name, ref):
    """ List the members of a specific dimension or the distinct values of a
    given attribute. """
    cube = get_cube(name)
    result = cube.members(ref, cuts=request.args.get('cut'),
                          order=request.args.get('order'),
                          page=request.args.get('page'),
                          page_size=request.args.get('pagesize'))
    result['status'] = 'ok'
    return jsonify(result)
