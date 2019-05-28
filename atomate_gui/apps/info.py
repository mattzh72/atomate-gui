from atomate_gui.app import app, collection
from atomate_gui.components.table import CollectionTable
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


class InfoApp:
    default_display_fields = [
        'spacegroup.number',
        'spacegroup.crystal_system',
        'bandstructure.is_metal',
        'structure.lattice.volume',
        'bandstructure.bandgap',
        'bandstructure.is_gap_direct'
    ]

    @staticmethod
    def serve_layout(pathname):
        entry = InfoApp.get_entry(pathname)

        return html.Div(children=[
            html.H1(
                children="Structure " + entry['material_id'],
                style={
                    'width': '100%',
                    'margin-bottom': '10px',
                    'text-align': 'center'
                }
            ),
            html.Div(
                InfoApp.generate_dropdown(entry),
                style={
                    'width': '50%',
                    'margin-bottom': '20px',
                    'text-align': 'center',
                    'margin-left': '25%',
                }),
            html.Div(id='data-table'),
        ])

    @staticmethod
    def get_entry(pathname):
        material_id = pathname[1:]
        query = {'material_id': material_id}
        return collection.find(query)[0]

    @staticmethod
    def generate_dropdown(entry):
        flat_entry = CollectionTable.flatten(entry)
        options = []
        for post in flat_entry:
            if post[:1] != "_":
                options.append({
                    'label': post, 'value': post
                })

        return dcc.Dropdown(
            id='data-table-dropdown',
            options=options,
            multi=True,
            value=InfoApp.default_display_fields,
            placeholder="Select query fields...",
        )

    @staticmethod
    def get_dict_value(entry, flat_name):
        keys = flat_name.split(".")
        value = entry

        for key in keys:
            value = value[key]

        return value

    @staticmethod
    def generate_data_table(pathname, values):
        display_fields = {}
        entry = InfoApp.get_entry(pathname)

        for value in values:
            display_fields[value] = InfoApp.get_dict_value(entry, value)

        return CollectionTable.generate_details_table(display_fields)


@app.callback(Output('data-table', 'children'),
              [Input('url', 'pathname'),
               Input('data-table-dropdown', 'value')])
def display_data_table(pathname, values):
    if not pathname or len(pathname) <= 1 or pathname == '/search' or not values:
        raise PreventUpdate
    else:
        return InfoApp.generate_data_table(pathname, values)
