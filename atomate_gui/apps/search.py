import dash_core_components as dcc
import dash_html_components as html

from managers.component_manager import ComponentManager
from managers.callback_manager import CallbackManager
from managers.collection_manager import CollectionManager
from managers.query_manager import QueryManager

from app import app, collection, ids

collection_manager = CollectionManager(collection)

component_manager = ComponentManager()
component_manager.add_components(collection_manager)

query_manager = QueryManager()
query_values = QueryManager.default_query
field_values = QueryManager.default_fields


def layout():
    return html.Div(children=[
        html.Div(children=[
            html.H1(
                id='header',
                children='Materialize Searcher',
            ),

            html.Button('SEARCH', id=ids["btn"], style={
                'width': '40%',
                'margin-bottom': '20px',
            }),

            html.Div(
                id='query_components',
                children=[html.Div(
                    id=ids["components"],
                    style={
                        'margin-bottom': '10px',
                    }
                )],
                style={
                    'width': '90%',
                    'margin-left': '5%',
                    'margin-bottom': '20px',
                    'text-align': 'center',
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
        ],
            id="side-bar",
            style={
                'width': '400px',
                'height': 'calc(100% - 40px)',
                'margin-top': '20px',
                'margin-bottom': '20px',
                'margin-left': '20px',
                'text-align': 'center',
                'border-radius': '5px',
                'box-shadow': '0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.24)',
                'overflow': 'scroll',
                'position': 'fixed',
            }
        ),

        html.Div(
            children=[
                html.Div(
                    children=[component_manager.query_dropdown.generate_component(ids["query_dropdown"], query_values)],
                    style={
                        'width': '80%',
                        'margin-bottom': '10px',
                    }
                ),

                html.Div(
                    children=[component_manager.field_dropdown.generate_component(ids["field_dropdown"], field_values)],
                    style={
                        'width': '80%',
                        'margin-bottom': '40px',
                    }
                ),

                html.Div(
                    id='table-selectors',
                    children=[
                        html.Div(
                            id='table-row-selector',
                            children=[
                                dcc.Dropdown(
                                    id='table-row-dropdown',
                                    options=[
                                        {'label': '20', 'value': 20},
                                        {'label': '50', 'value': 50},
                                        {'label': '100', 'value': 100}
                                    ],
                                    value='50',
                                    clearable=False
                                )],
                        ),

                        html.Div(
                            id='table-page-selector',
                            children=[
                                html.Button('<', id='table-backward'),
                                html.Button('>', id='table-forward'),
                                html.Div('', id='table-page-index')
                            ]
                        )

                    ]

                ),

                html.Div(
                    id=ids["table_output"],
                    children='No table yet.',
                    style={
                        'width': '80%',
                        'text-align': 'center',
                        # 'border': '1px solid #D3D3D3',
                        # 'border-radius': '5px',
                    }
                )],

            style={
                'padding-top': '50px',
                'margin-left': 'calc(400px + 0.1 * (100% - 400px))',
                'height': '100vh',
                'width': 'calc(100% - 400px)',
            }
        )
    ])


callback_manager = CallbackManager(app, component_manager, query_manager)
callback_manager.attach_callbacks()
