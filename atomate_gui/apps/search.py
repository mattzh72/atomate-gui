import dash_core_components as dcc
import dash_html_components as html

from managers.component_manager import ComponentManager
from managers.callback_manager import CallbackManager
from managers.collection_manager import CollectionManager

from app import app, collection, ids

collection_manager = CollectionManager(collection)

component_manager = ComponentManager()
component_manager.add_components(collection_manager)

query_values = [
    "['nelements']",
    "['material_id']",
    "['spacegroup']['number']",
    "['stability']['e_above_hull']",
    "['bandstructure']['is_gap_direct']",
    "['chemsys']"
]

field_values = [
    "['chemsys']",
    "['bandgap']",
    "['material_id']"
]


def layout():
    return html.Div(children=[
        html.H1(
            children='Materialize Search Engine',
            style={
                'width': '100%',
                'margin-bottom': '70px',
                'margin-top': '20px',
                'text-align': 'center'}
            ),

        html.Div(
            children=[component_manager.query_dropdown.generate_component(ids["query_dropdown"], query_values)],
            style={
                'width': '50%',
                'margin-left': '25%',
                'margin-bottom': '20px',
            }
        ),

        html.Div(
            children=[component_manager.field_dropdown.generate_component(ids["field_dropdown"], field_values)],
            style={
                'width': '50%',
                'margin-left': '25%',
                'margin-bottom': '20px',
            }
        ),

        html.Div(
            id='query_components',
            children=[html.Div(
                        id=ids["components"],
                        children=[],
                        style={
                            'margin-bottom': '10px',
                        }
                    ),
                    html.Button('Search', id=ids["btn"], style={
                            'margin-bottom': '20px',
                        }),
                ],
            style={
                'width': '90%',
                'margin-left': '5%',
                'margin-bottom': '20px',
                'text-align': 'center',
                # 'border': '1px solid #D3D3D3',
                # 'border-radius': '5px',
            }
        ),

        dcc.Input(
            id=ids["query_input"],
            placeholder='',
            type='text',
            value='',
            style={
                'width': '60%',
                'margin-bottom': '10px',
                'margin-left': '20%',
                'display': 'none',
            },
        ),

        dcc.Input(
            id=ids["fields_input"],
            placeholder='Put the fields you want to display here...',
            type='text',
            value="",
            style={
                'width': '60%',
                'margin-bottom': '20px',
                'margin-left': '20%',
                'display': 'none',
            },
        ),

        html.Div(
            id=ids["table_output"],
            children='No table yet.',
            style={
                'padding': '20px'
            }
        ),
    ])


callback_manager = CallbackManager(app, component_manager)
callback_manager.attach_callbacks()
