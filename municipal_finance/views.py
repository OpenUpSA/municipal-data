from django.http import Http404
from django.shortcuts import render

from .cubes import get_manager
from .utils import jsonify, serialize, check_page_size


from django.views.decorators.clickjacking import xframe_options_exempt


DUMP_FORMATS = ['csv', 'xlsx']
FORMATS = DUMP_FORMATS + ['json']


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


def get_cube_with_last_updated(connection, manager, name):
    model = manager.get_cube(name).model.to_dict()
    updates_table = model.get("updates_table")
    if updates_table:
        result = connection.execute(
            f"SELECT datetime FROM {updates_table} ORDER BY datetime DESC LIMIT 1"
        ).first()
        if result is not None:
            model["last_updated"] = result[0].strftime("%Y-%m")
    return model


@xframe_options_exempt
def index(request):
    manager = get_manager()
    cube_names = manager.list_cubes()
    with manager.get_engine().connect() as connection:
        # Collect details for all cubes
        cubes = list(
            map(
                lambda name: (
                    name,
                    get_cube_with_last_updated(connection, manager, name),
                ),
                cube_names,
            )
        )

        v1_year = "2009-10 to 2018-19"
        v2_year = "2019-20 onwards"

        cube_map = {
            "Aged Creditor Analysis" : [("aged_creditor", "V1", v1_year), ("aged_creditor_v2", "V2", v2_year)],
            "Aged Debtor Analysis" : [("aged_debtor", "V1", v1_year), ("aged_debtor_v2", "V2", v2_year)],
            "Audit Opinions" : [("audit_opinions", "", "2009-10 onwards", "no_data")],
            "Financial Position" : [("bsheet", "V1", v1_year), ("financial_position_v2", "V2", v2_year)],
            "Capital Aquisition" : [("capital", "V1", v1_year), ("capital_v2", "V2", v2_year)],
            "Cash Flow" : [("cflow", "V1", v1_year), ("cflow_v2", "V2", v2_year)],
            "Grants" : [("conditional_grants", "V1", v1_year, "no_data"), ("grants_v2", "V2", v2_year, "no_data")],
            "Demarcation Changes" : [("demarcation_changes", "", "2009-10 onwards", "no_data")],
            "Income and Expenditure" : [("incexp", "V1", v1_year), ("incexp_v2", "V2", v2_year)],
            "Municipal Officials" : [("officials", "", "2009-10 onwards", "no_data")],
            "Municipalities" : [("municipalities", "", "2009-10 onwards", "no_data")],
            "Reparis and Maintenance" : [("repmaint", "V1", v1_year), ("repmaint_v2", "", v2_year)],
            "Unauthorised Irregular Fruitless and Wasteful Expenditure" : [("uifwexp", "", "2009-10 onwards")]
        }

    return render(request, 'index.html', {
        'cubes': [cubes],
        'cubes_new': cubes,
        'cube_count': len(cube_names),
        'cube_map' : cube_map,
    })


@xframe_options_exempt
def docs(request):
    manager = get_manager()
    cubes = []
    for cube_name in manager.list_cubes():
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
    for name in manager.list_cubes():
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
    manager = get_manager()
    with manager.get_engine().connect() as connection:
        model = get_cube_with_last_updated(connection, manager, cube_name)
    return jsonify({
        'status': 'ok',
        'name': cube_name,
        'model': model
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
    for name in manager.list_cubes():
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
