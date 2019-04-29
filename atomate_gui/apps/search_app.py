import dash_core_components as dcc
import dash_html_components as html

from managers.component_manager import ComponentManager
from managers.callback_manager import CallbackManager
from managers.collection_manager import CollectionManager
from managers.query_manager import QueryManager

from app import app, collection, ids


class SearchApp:
    clm = CollectionManager(collection)

    cpm = ComponentManager()
    cpm.add_components(clm)

    qm = QueryManager()
    query_values = QueryManager.default_query
    field_values = QueryManager.default_fields

    clb = CallbackManager(app, cpm, qm)

    @staticmethod
    def serve_layout():
        return html.Div(id='main',children=[
            html.Div(
                id="side-bar",
                children=[
                    html.Button('SEARCH', id=ids["btn"]),

                    html.Div(
                        id='query_components',
                        children=[html.Div(
                            id=ids["components"],
                            style={
                                'margin-bottom': '10px',
                            }
                        )],
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
                        }
                    )]
            ),

            html.Div(
                id='search-main',
                children=[
                    html.Div(
                        SearchApp.cpm.query_dropdown.generate_component('query-dropdown', SearchApp.query_values),
                    ),

                    html.Div(
                        SearchApp.cpm.field_dropdown.generate_component('field-dropdown', SearchApp.field_values),
                    ),

                    html.Div(
                        id='table-selectors',
                        children=[
                            html.Div(
                                id='row-count-selector',
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
                                    html.Div('', id='table-page-index'),
                                    html.Button('<', id='table-backward'),
                                    html.Button('>', id='table-forward'),
                                ])
                        ]),

                    html.Div(
                        id=ids["table_output"],
                    )],
            )
        ])
