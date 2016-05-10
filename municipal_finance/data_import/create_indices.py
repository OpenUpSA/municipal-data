from municipal_finance.cubes import cube_manager


def create_index_statements():
    with open('sql/create_indices.sql', 'w') as f:
        for cube_name in cube_manager.list_cubes():
            cube = cube_manager.get_cube(cube_name)
            model = cube.model.to_dict()
            for dimension_name, dimension in model['dimensions'].iteritems():
                attribute_names = dimension['attributes'].keys()
                table_name = model['fact_table']

                # create per-attribute index
                for attribute_name in attribute_names:
                    column = dimension['attributes'][attribute_name]['column']
                    f.write("CREATE INDEX %s_%s_idx ON %s (%s);\n"
                          % (table_name, column, table_name, column))

                if len(attribute_names) > 1:
                    # create dimension index
                    column_str = ", ".join(map(lambda a: dimension['attributes'][a]['column'],
                                               sorted(attribute_names)))
                    f.write("CREATE INDEX %s_dimension_%s_idx ON %s (%s);\n"
                          % (table_name, dimension_name, table_name, column_str))

                if dimension_name == "item":
                    rest = list(attribute_names)
                    rest.remove("position_in_return_form")
                    column_str = ", ".join(map(lambda a: dimension['attributes'][a]['column'],
                                               (["position_in_return_form"] + sorted(rest))))
                    f.write("CREATE INDEX %s_item_ordered_idx ON %s (%s);\n"
                          % (table_name, table_name, column_str))
