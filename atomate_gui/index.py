import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import crystal_toolkit.components as ct
from pymatgen import Structure

from app import app, collection
from apps import search, data


ct.register_app(app)
struct_component = ct.StructureMoleculeComponent()
struct_layout = html.Div([
            struct_component.standard_layout,
            struct_component.all_layouts["title"],
            struct_component.all_layouts["legend"],
            struct_component.all_layouts["options"],
            struct_component.all_layouts["screenshot"]
])


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    ct.MPComponent.all_app_stores(),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if not pathname or len(pathname) <= 1:
        raise PreventUpdate
    elif pathname == '/search':
        return html.Div(search.layout(),
                        html.Div(struct_layout, style={"display": "none"}))
    else:
        return html.Div(struct_layout, style={"display": "block"})


@app.callback(
    Output(struct_component.id(), "data"),
    [Input('url', 'pathname')]
)
def update_structure(pathname):
    if not pathname or pathname == '/search':
        raise PreventUpdate
    material_id = pathname[1:]
    query = {'material_id': material_id}
    entries = collection.find(query)

    structure = Structure.from_dict(entries[0]["structure"])
    return struct_component.to_data(structure)


if __name__ == '__main__':
    app.run_server(debug=True)

