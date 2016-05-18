"""
  from municipal_finance.data_import import create_indices as ci
"""

from municipal_finance.cubes import cube_manager


def create_index_statements():
    with open('sql/create_indices.sql', 'w') as f:
        for cube_name in cube_manager.list_cubes():
            f.write("\\echo cube=%s\n" % cube_name)
            cube = cube_manager.get_cube(cube_name)
            model = cube.model.to_dict()
            for dimension_name, dimension in model['dimensions'].iteritems():
                f.write("\\echo dimension=%s\n" % dimension_name)

                attribute_names = dimension['attributes'].keys()
                fact_table_name = model['fact_table']

                f.write("\\echo attributes\n")
                for attribute_name in attribute_names:
                    attribute_column_index(f,
                                           fact_table_name,
                                           dimension,
                                           attribute_name)

                if len(attribute_names) > 1:
                    f.write("\\echo dimension\n")
                    dimension_index(f,
                                    fact_table_name,
                                    dimension,
                                    dimension_name,
                                    attribute_names)

                if dimension_name == "item":
                    f.write("\\echo dimension positional\n")
                    dimension_positional_index(f,
                                               fact_table_name,
                                               dimension,
                                               dimension_name,
                                               attribute_names)
        f.write("\n")


def attribute_column_index(f, fact_table_name, dimension, attribute_name):
    column_ref = dimension['attributes'][attribute_name]['column']
    table_name, column_name = qualify(fact_table_name, column_ref)
    f.write("CREATE INDEX %s_%s_idx ON %s (%s);\n"
            % (table_name, column_name, table_name, column_name))


def dimension_index(f, fact_table_name, dimension, dimension_name, attribute_names):
    some_column_ref = dimension['attributes'][attribute_names[0]]['column']
    table_name, column_name = qualify(fact_table_name, some_column_ref)

    column_str = ", ".join(map(attr_column_f(fact_table_name, dimension),
                               sorted(attribute_names)))
    f.write("CREATE INDEX %s_dimension_%s_idx ON %s (%s);\n"
            % (table_name, dimension_name, table_name, column_str))


def dimension_positional_index(f, fact_table_name, dimension, dimension_name, attribute_names):
    # create dimension index starting with position_in_return_form
    rest = [a for a in list(attribute_names) if 'position_in_return_form' not in a]
    some_column_ref = dimension['attributes'][rest[0]]['column']
    table_name, column_name = qualify(fact_table_name, some_column_ref)

    column_str = ", ".join(map(attr_column_f(fact_table_name, dimension),
                               (['position_in_return_form'] + sorted(rest))))
    f.write("CREATE INDEX %s_position_ordered_idx ON %s (%s);\n"
            % (table_name, table_name, column_str))


def attr_column_f(fact_table_name, dimension):
    return lambda a: (qualify(fact_table_name, dimension['attributes'][a]['column']))[1]


def qualify(fact_table_name, column_ref):
    if '.' in column_ref:
        return column_ref.split('.', 1)
    else:
        return fact_table_name, column_ref
