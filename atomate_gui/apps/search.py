import dash_html_components as html
import dash_table
from atomate_gui.managers.component_manager import ComponentManager
from atomate_gui.managers.collection_manager import CollectionManager


class SearchApp:
    default_query = [
        "['nelements']",
        "['material_id']",
        "['spacegroup']['number']",
        "['stability']['e_above_hull']",
        "['bandstructure']['is_gap_direct']",
        "['chemsys']"
    ]
    default_fields = [
        "['chemsys']",
        "['bandgap']",
        "['material_id']",
        "['stability']['e_above_hull']",
    ]

    clm = CollectionManager()
    cpm = ComponentManager()
    cpm.add_components(clm)
    cpm.attach_callbacks()

    @staticmethod
    def serve_layout():
        return html.Div(id='main', children=[
            html.Div(
                id="side-bar",
                children=[
                    html.Button('SEARCH', id='search-button'),

                    html.Div(
                        id='query_components',
                        children=[html.Div(
                            id='components-container',
                            style={
                                'margin-bottom': '10px',
                            }
                        )],
                    )]
            ),

            html.Div(
                id='search-main',
                children=[
                    html.Div(
                        SearchApp.cpm.query_dd.generate_component('query-dropdown', SearchApp.default_query),
                    ),

                    html.Div(
                        SearchApp.cpm.field_dd.generate_component('field-dropdown', SearchApp.default_fields),
                    ),

                    html.Div(
                        dash_table.DataTable(
                            id='search-table',
                            columns=[],
                            data=[],
                            sorting=True,
                            sorting_type="multi",
                            pagination_mode="fe",
                            style_as_list_view=True,
                            style_cell={
                                'padding': '10px',
                                'font-family': 'Helvetica',
                                'font-size': '15px',
                            },
                            style_cell_conditional=[
                                {
                                    'if': {'column_type': 'any'},
                                    'textAlign': 'left'
                                },
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                                }
                            ],
                            style_header={
                                'color': 'black',
                                'font-family': 'Helvetica',
                                'font-size': '17px',
                                'fontWeight': 'bold',
                            },
                            pagination_settings={
                                "current_page": 0,
                                "page_size": 50,
                            },
                            style_table={
                                'overflowX': 'scroll'
                            },
                        ),
                        id='search-table-wrapper'
                    )],
            )
        ])
