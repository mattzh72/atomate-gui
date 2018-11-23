from dash.dependencies import Input, Output
from queries import generate_slider_query
from utils import generate_table, query_input_id, fields_input_id, table_output_id, ROW_LABEL
import pandas as pd
import ast


def create_callback(component_type, data, output_id):
    def callback(value, component_id):
        if component_type == 'range-slider':
            if 'output' in output_id:
                return 'You have selected {} for {}'.format(value, component_id)
            elif 'query' in output_id:
                return generate_slider_query(data['name'], value[0], value[1])

    return callback


def generate_callbacks(queries, collection, app):
    fields_dict = classify_type(queries, collection, verbose=False)

    for component, fields in fields_dict.items():
        for field in fields:
            output_callback = create_callback(component, field, 'output')
            app.callback(
                Output(field['name']+'-output-container', 'children'),
                [Input(field['name'], 'value'), Input(field['name'], 'id')]
            )(output_callback)
    #
            query_callback = create_callback(component, field, 'query')
            app.callback(
                Output(query_input_id, 'value'),
                [Input(field['name'], 'value'), Input(field['name'], 'id')]
            )(query_callback)

        generate_table_callback(app, collection)


def generate_table_callback(app, collection):
    table_callback = create_table_callback(collection)



def create_table_callback(collection):

    def callback(query, fields_arr):
        try:
            mat_structs = {}

            for post in collection.find(ast.literal_eval(query), ast.literal_eval(fields_arr)):
                mat_structs[post[ROW_LABEL]] = post

            for mat in mat_structs:
                for descrips in mat_structs[mat]:
                    if isinstance(mat_structs[mat][descrips], dict):
                        mat_structs[mat][descrips] = str(mat_structs[mat][descrips])

            df = pd.DataFrame.from_dict(mat_structs, orient='index')
            return [generate_table(df)]
        except Exception as e:
            return

    return callback


def get_all_field_names(collection):
    sample_entry = collection.find_one()
    return sample_entry.keys()

def generate_all_callbacks(collection, app):
    generate_callbacks(get_all_field_names(collection), collection, app)
    generate_table_callback(app, collection)

def generate_slider_query(name, min_val, max_val):
    return "{{'{0}': {{'$gte': {1}, '$lte': {2}}}}}".format(name, min_val, max_val)

