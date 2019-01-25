import dash_core_components as dcc
import dash_html_components as html

from managers.component_manager import ComponentManager
from managers.callback_manager import CallbackManager
from managers.collection_manager import CollectionManager

from app import app, collection, ids

collection_manager = CollectionManager(collection)

component_manager = ComponentManager()
component_manager.add_components(collection_manager)


def layout():
    return html.Div(children=[
        html.H1(
            children='Materialize Search Engine',
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

        html.Div(
            id='query_components',
            children=[
                    html.Div(
                        children='Control Suite',
                        style={
                            'width': '100%',
                            'margin-bottom': '10px',
                            'margin-top': '10px',
                            'text-align': 'center'
                        }
                    ),
                    html.Div(
                        children=[component_manager.dropdown.generate_component()],
                        style={
                            'width': '80%',
                            'margin-left': '10%',
                            'margin-bottom': '10px',
                            'margin-top': '10px',
                        }
                    ),
                    html.Div(
                        id=ids["component_container"],
                        children=[],
                        style={
                            'width': '80%',
                            'margin-left': '10%',
                            'border': '1px solid #D3D3D3',
                            "border-radius": "5px",
                            'margin-bottom': '20px',
                            'padding-top': '10px',
                        }
                    ),
                ],
            style={
                'width': '50%',
                'margin-left': '25%',
                'margin-bottom': '20px',
                'text-align': 'center',
                'border': '1px solid #D3D3D3',
                "border-radius": "5px",
            }
        ),

        dcc.Input(
            id=ids["query_input"],
            placeholder='Put a query here...',
            type='text',
            value="{'nelements': {'$gte': 6, '$lte': 8}}",
            style={
                'width': '60%',
                'margin-bottom': '10px',
                'margin-left': '20%'
            },
        ),

        dcc.Input(
            id=ids["fields_input"],
            placeholder='Put the fields you want to display here...',
            type='text',
            value="{'bandgap': 1, 'chemsys': 1, 'bandstructure': 1, 'material_id': 1, '_id': 0}",
            style={
                'width': '60%',
                'margin-bottom': '20px',
                'margin-left': '20%'
            },
        ),

        html.Div(
            id=ids["table_output"],
            children='No table yet.',
            )
    ])


callback_manager = CallbackManager()
callback_manager.generate_all_io(component_manager)
callback_manager.attach_callbacks(app)
