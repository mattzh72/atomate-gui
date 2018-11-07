from layouts.table import serve_layout, queries, fields, collection
from utils import generate_table
import pandas as pd
from dash.dependencies import Input, Output
import ast
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = serve_layout

ROW_LABEL = "chemsys"
query_input_id = "query-input"
fields_input_id = "field_input"
textarea_output_id = "textarea_output"
table_output_id = "table_output"

@app.callback(
    Output(component_id=table_output_id, component_property='children'),
    [
        Input(component_id=query_input_id, component_property='value'),
        Input(component_id=fields_input_id, component_property='value')
    ]
)
def update_textarea_output_div(query, fields):
    try:
        mat_structs = {}

        for post in collection.find(ast.literal_eval(query), ast.literal_eval(fields)):
            mat_structs[post[ROW_LABEL]] = post

        for mat in mat_structs:
            for descrips in mat_structs[mat]:
                if isinstance(mat_structs[mat][descrips], dict):
                    mat_structs[mat][descrips] = str(mat_structs[mat][descrips])

        df = pd.DataFrame.from_dict(mat_structs, orient='index')
        return [generate_table(df)]
    except Exception as e:
        return


@app.callback(
    Output(component_id=queries[0] + '-output-container-range-slider', component_property='children'),
    [Input(component_id=queries[0] + '-range-slider', component_property='value')])
def update_output(value):
    return 'You have selected {} for {}'.format(value, queries[0])

@app.callback(
    Output(component_id=query_input_id, component_property='value'),
    [Input(component_id=queries[0] + '-range-slider', component_property='value')])
def update_output(value):
    return '{{"nelements": {{"$gte": {0}, "$lte": {1}}}}}'.format(value[0], value[1])





if __name__ == '__main__':
    app.run_server(debug=True)
