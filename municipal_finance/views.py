from django.http import Http404
from django.shortcuts import render

from .cubes import get_manager
from .utils import jsonify, serialize, check_page_size


from django.views.decorators.clickjacking import xframe_options_exempt


DUMP_FORMATS = ['csv', 'xlsx']
FORMATS = DUMP_FORMATS + ['json']
HIDDEN_CUBES = ['bsheet_v2', 'cflow_v2', 'incexp_v2']


def list_cube_names(manager):
    cube_names = manager.list_cubes()
    # Filter out hidden cubes
    cube_names = list(
        filter(
            lambda name: name not in HIDDEN_CUBES,
            cube_names
        )
    )
    # Return the list of cube names
    return cube_names


def get_cube(name):
    """ Load the named cube from the current registered ``CubeManager``. """
    if not get_manager().has_cube(name):
        raise Http404('No such cube: %s' % name)
    return get_manager().get_cube(name)


def get_format(request):
    format = request.GET.get('format', 'json')
    if format in FORMATS:
        return format
    raise Http404()


@xframe_options_exempt
def index(request):
    manager = get_manager()
    cube_names = list_cube_names(manager)
    # Collect details for all cubes
    cubes = [(c, manager.get_cube(c).model.to_dict()) for c in cube_names]
    cubes = sorted(cubes, key=lambda p: p[1]['label'])
    # Group into rows of four
    cubes = [cubes[i:i + 4] for i in range(0, len(cubes), 4)]
    return render(request, 'index.html', {
        'cubes': cubes,
        'cube_count': len(cube_names),
    })


@xframe_options_exempt
def docs(request):
    manager = get_manager()
    cubes = []
    for cube_name in list_cube_names(manager):
        cube = manager.get_cube(cube_name)
        (model,) = cube.model.to_dict(),
        if 'item' in model['dimensions'].keys():
            if 'position_in_return_form' \
               in model['dimensions']['item']['attributes'].keys():
                items = cube.members('item',
                                     order='item.position_in_return_form:asc')['data']
            else:
                items = cube.members('item')['data']
        else:
            items = None
        cubes.append({
            'model': model,
            'name': cube_name,
            'items': items,
        })

    return render(request, 'docs.html', {
        'cubes': cubes,
    })


@xframe_options_exempt
def embed(request, cube_name):
    return render(request, 'embed.html')


@xframe_options_exempt
def status(request):
    """ General system status report :) """
    from babbage import __version__, __doc__
    return jsonify({
        'status': 'ok',
        'api': 'babbage',
        'message': __doc__,
        'version': __version__
    })


@xframe_options_exempt
def api_root(request):
    """
    List available endpoints.
    """
    endpoints = [
        request.build_absolute_uri('/api/cubes'),
    ]
    return jsonify({
        'endpoints': endpoints,
        'documentation': 'https://municipaldata.treasury.gov.za/docs',
    })


@xframe_options_exempt
def cubes(request):
    """ Get a listing of all publicly available cubes. """
    manager = get_manager()
    cubes = []
    for name in list_cube_names(manager):
        cube = manager.get_cube(name)
        cubes.append({
            'name': name,
            'label': cube.model.spec['label'],
            'description': cube.model.spec['description'],
            'uri': request.build_absolute_uri() + '/' + name,
        })
    return jsonify({
        'status': 'ok',
        'data': cubes
    })


@xframe_options_exempt
def cube_root(request, cube_name):
    """
    List available endpoints.
    """
    uri = request.build_absolute_uri()
    endpoints = [
        uri + '/model',
        uri + '/members',
        uri + '/facts',
        uri + '/aggregate',
    ]
    return jsonify({
        'endpoints': endpoints,
        'documentation': 'https://municipaldata.treasury.gov.za/docs',
    })


@xframe_options_exempt
def model(request, cube_name):
    """ Get the model for the specified cube. """
    cube = get_cube(cube_name)
    return jsonify({
        'status': 'ok',
        'name': cube_name,
        'model': cube.model
    })


@xframe_options_exempt
def aggregate(request, cube_name):
    """ Perform an aggregation request. """
    cube = get_cube(cube_name)
    format = get_format(request)
    page_size = check_page_size(request.GET.get('pagesize'))
    page_max = page_size if format in DUMP_FORMATS else 20000
    result = cube.aggregate(aggregates=request.GET.get('aggregates'),
                            drilldowns=request.GET.get('drilldown'),
                            cuts=request.GET.get('cut'),
                            order=request.GET.get('order'),
                            page=request.GET.get('page'),
                            page_size=page_size,
                            page_max=page_max)
    if format == 'json':
        result['status'] = 'ok'
        return jsonify(result)
    elif format in DUMP_FORMATS:
        fields = result['attributes'] + result['aggregates']
        return serialize(format, cube_name + '_aggregate', fields, result['cells'])


@xframe_options_exempt
def facts(request, cube_name):
    """ List the fact table entries in the current cube. This is the full
    materialized dataset. """
    cube = get_cube(cube_name)
    format = get_format(request)
    page_size = check_page_size(request.GET.get('pagesize'))
    page_max = page_size if format in DUMP_FORMATS else 10000
    result = cube.facts(fields=request.GET.get('fields'),
                        cuts=request.GET.get('cut'),
                        order=request.GET.get('order'),
                        page=request.GET.get('page'),
                        page_size=page_size,
                        page_max=page_max)
    if format == 'json':
        result['status'] = 'ok'
        return jsonify(result)
    elif format in DUMP_FORMATS:
        return serialize(format, cube_name + '_facts', result['fields'], result['data'])


@xframe_options_exempt
def members_root(request, cube_name):
    cube = get_manager().get_cube(cube_name)
    (model,) = cube.model.to_dict(),
    members = model['dimensions'].keys()
    uri = request.build_absolute_uri()
    endpoints = [uri + '/' + member for member in members]
    return jsonify({
        'endpoints': endpoints,
        'documentation': 'https://municipaldata.treasury.gov.za/docs',
    })


@xframe_options_exempt
def members(request, cube_name, member_ref):
    """ List the members of a specific dimension or the distinct values of a
    given attribute. """
    cube = get_cube(cube_name)
    format = get_format(request)
    page_size = check_page_size(request.GET.get('pagesize'))
    result = cube.members(member_ref,
                          cuts=request.GET.get('cut'),
                          order=request.GET.get('order'),
                          page=request.GET.get('page'),
                          page_size=page_size)
    if format == 'json':
        result['status'] = 'ok'
        return jsonify(result)
    elif format in DUMP_FORMATS:
        return serialize(format, cube_name + '_members', result['fields'], result['data'])


@xframe_options_exempt
def table(request, cube_name):
    manager = get_manager()
    cubes = {}
    for name in list_cube_names(manager):
        if name not in ['municipalities', 'officials']:
            cubes[name] = {
                'model': manager.get_cube(name).model.to_dict(),
                'name': name,
            }
    cube = manager.get_cube(cube_name).model.to_dict()
    return render(request, 'table.html', {
        'cube_name': cube_name,
        'cube_model': cube,
        'cubes': cubes,
    })
