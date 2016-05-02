from django.http import Http404
from django.shortcuts import render, redirect
from cubes import cube_manager

from utils import jsonify, csvify

from django.views.decorators.clickjacking import xframe_options_exempt


def get_cube(name):
    """ Load the named cube from the current registered ``CubeManager``. """
    if not cube_manager.has_cube(name):
        raise Http404('No such cube: %s' % name)
    return cube_manager.get_cube(name)


@xframe_options_exempt
def index(request):
    cubes = []
    for cube_name in cube_manager.list_cubes():
        cube = cube_manager.get_cube(cube_name)
        (model,) = cube.model.to_dict(),
        if 'item' in model['dimensions'].keys():
            items = cube.members('item', order='item.position_in_return_form:asc')['data']
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
def docs(request):
    return redirect('/')


@xframe_options_exempt
def explore(request, cube_name):
    cubes = []
    for name in cube_manager.list_cubes():
        cubes.append({
            'model': cube_manager.get_cube(name).model.to_dict(),
            'name': name,
        })
    cube = cube_manager.get_cube(cube_name).model.to_dict()
    return render(request, 'explore.html', {
        'cube_name': cube_name,
        'cube_model': cube,
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
def cubes(request):
    """ Get a listing of all publicly available cubes. """
    cubes = []
    for name in cube_manager.list_cubes():
        cube = cube_manager.get_cube(name)
        cubes.append({
            'name': name,
            'label': cube.model.spec['label'],
            'description': cube.model.spec['description'],
        })
    return jsonify({
        'status': 'ok',
        'data': cubes
    })


@xframe_options_exempt
def model(request, cube_name):
    """ Get the model for the specified cube. """
    cube = get_cube(cube_name)
    cube.compute_cardinalities()
    return jsonify({
        'status': 'ok',
        'name': cube_name,
        'model': cube.model
    })


@xframe_options_exempt
def aggregate(request, cube_name):
    """ Perform an aggregation request. """
    cube = get_cube(cube_name)
    format = request.GET.get('format', 'json')
    page_max = request.GET.get('pagesize') if format == 'csv' else 10000
    result = cube.aggregate(aggregates=request.GET.get('aggregates'),
                            drilldowns=request.GET.get('drilldown'),
                            cuts=request.GET.get('cut'),
                            order=request.GET.get('order'),
                            page=request.GET.get('page'),
                            page_size=request.GET.get('pagesize'),
                            page_max=page_max)
    if format == 'json':
        result['status'] = 'ok'
        return jsonify(result)
    elif format == 'csv':
        fields = result['attributes'] + result['aggregates']
        return csvify(cube_name + '_aggregate', fields, result['cells'])


@xframe_options_exempt
def facts(request, cube_name):
    """ List the fact table entries in the current cube. This is the full
    materialized dataset. """
    cube = get_cube(cube_name)
    format = request.GET.get('format', 'json')
    page_max = request.GET.get('pagesize') if format == 'csv' else 10000
    result = cube.facts(fields=request.GET.get('fields'),
                        cuts=request.GET.get('cut'),
                        order=request.GET.get('order'),
                        page=request.GET.get('page'),
                        page_size=request.GET.get('pagesize'),
                        page_max=page_max)
    if format == 'json':
        result['status'] = 'ok'
        return jsonify(result)
    elif format == 'csv':
        return csvify(cube_name + '_facts', result['fields'], result['data'])


@xframe_options_exempt
def members(request, cube_name, member_ref):
    """ List the members of a specific dimension or the distinct values of a
    given attribute. """
    cube = get_cube(cube_name)
    format = request.GET.get('format', 'json')
    page_max = request.GET.get('pagesize') if format == 'csv' else 10000
    result = cube.members(member_ref,
                          cuts=request.GET.get('cut'),
                          order=request.GET.get('order'),
                          page=request.GET.get('page'),
                          page_size=request.GET.get('pagesize'))
    if format == 'json':
        result['status'] = 'ok'
        return jsonify(result)
    elif format == 'csv':
        return csvify(cube_name + '_members', result['fields'], result['data'])


@xframe_options_exempt
def table(request, cube_name):
    cubes = []
    for name in cube_manager.list_cubes():
        if name not in ['municipalities', 'officials']:
            cubes.append({
                'model': cube_manager.get_cube(name).model.to_dict(),
                'name': name,
            })

    cube = cube_manager.get_cube(cube_name).model.to_dict()
    return render(request, 'table.html', {
        'cube_name': cube_name,
        'cube_model': cube,
        'cubes': cubes,
    })
