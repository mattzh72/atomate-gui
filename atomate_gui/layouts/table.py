from atomate_gui.utils import insert_components
from atomate_gui.app import collection
import dash_core_components as dcc
import dash_html_components as html

queries = ["nelements"]
fields = ["bandgap", "chemsys"]

ROW_LABEL = "chemsys"

query_input_id = "query-input"
fields_input_id = "field_input"
textarea_output_id = "textarea_output"
table_output_id = "table_output"


def serve_layout():
    return html.Div(children=[
    html.H1(
        children='Materials DB Web UI',
        style={
            'width': '100%',
            'margin-bottom': '10px',
            'margin-top': '20px',
            'text-align': 'center'}
        ),

    html.Div(
        children='This application queries the materials database.',
        style={
            'width': '100%',
            'margin-bottom': '20px',
            'text-align': 'center'
            }
        ),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select YAML File')
        ]),
        style={
            'width': '60%',
            'margin-bottom': '10px',
            'margin-left': '20%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),

    insert_components(queries, fields, collection),

    dcc.Input(
        id=query_input_id,
        placeholder='Put a query here...',
        type='text',
        value="{'nelements':4}",
        style={
            'width': '60%',
            'margin-bottom': '10px',
            'margin-left': '20%'},
    ),

    dcc.Input(
        id=fields_input_id,
        placeholder='Put the fields you want to display here...',
        type='text',
        value="{'bandgap': 1, 'chemsys': 1, 'bandstructure': 1, '_id': 0}",
        style={
            'width': '60%',
            'margin-bottom': '20px',
            'margin-left': '20%'
            },
    ),

    html.Div(
        id=table_output_id,
        children='No table yet.',
        )
    ])
