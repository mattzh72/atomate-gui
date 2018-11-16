import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from queries import generate_slider_query
from utils import generate_table, query_input_id, fields_input_id, table_output_id, ROW_LABEL
import pandas as pd
import ast


def classify_type(field_names, collection, verbose=True):
    fields_dict = {'range-slider': [], 'input': []}
    for field_name in field_names:
        first_entry = collection.find_one()[field_name]

        if isinstance(first_entry, int) or isinstance(first_entry, float):
            min_val, max_val = detect_range(field_name, collection)
            step = 1

            if isinstance(first_entry, float):
                step = (max_val - min_val) / 100

            if verbose:
                fields_dict['range-slider'].append({'name': field_name, 'range': [min_val, max_val], 'step': step})
            else:
                fields_dict['range-slider'].append({'name': field_name})
        elif isinstance(first_entry, str):
            fields_dict['input'].append({'name': field_name})

    return fields_dict


def detect_range(field_name, collection):
    max_val, min_val = float('-inf'), float('inf')

    for post in collection.find():
        val = post[field_name]

        if val > max_val:
            max_val = val

        if val < min_val:
            min_val = val

    return min_val, max_val


def choose_component(key, value):
    if key == 'range-slider':
        return html.Div(
            children=[dcc.RangeSlider(
                id=value['name'],
                className=key,
                count=1,
                min=value['range'][0],
                max=value['range'][1],
                step=value['step'],
                value=value['range']
            ),
                html.Div(
                    id=value['name'] + '-output-container'
                )
            ]
        )
    elif key == 'input':
        return html.Div(
            children=[dcc.Input(
                id=value['name'],
                className=key,
                placeholder='Enter a value for ' + value['name'],
                type='text',
                value=''
            ),
                html.Div(
                    id=value['name'] + '-output-container'
                )
            ]
        )


def insert_components(queries, collection):
    fields_dict = classify_type(queries, collection)
    children_list = []

    for key, values in fields_dict.items():
        for value in values:
            children_list.append(choose_component(key, value))

    return html.Div(
        id='query_components',
        children=children_list,
        style={
            'width': '50%',
            'margin-bottom': '20px',
            'text-align': 'center',
        }
    )


def create_callback(component_type, data, output_id):

    def callback(value, id):
        if component_type == 'range-slider':
            if 'output' in output_id:
                return 'You have selected {} for {}'.format(value, id)
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
    app.callback(
        Output(table_output_id, 'children'),
        [
            Input(query_input_id, 'value'),
            Input(fields_input_id, 'value')
        ]
    )(table_callback)


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

