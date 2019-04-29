import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import crystal_toolkit.components as ct
from pymatgen import Structure

from app import app, collection
from apps.data_app import DataApp
from apps.search_app import SearchApp

ct.register_app(app)
struct_component = ct.StructureMoleculeComponent()
struct_layout = html.Div([
    html.Div(),
    html.Div([
        struct_component.all_layouts["title"],
        struct_component.all_layouts["legend"],
        struct_component.all_layouts["options"],
        struct_component.all_layouts["screenshot"]],
    )],
    id='visualizer',
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    ct.MPComponent.all_app_stores(),
    html.Div(
        id='header',
        children=html.H1(
            'Materials Searcher.',
        ),
    ),
    html.Div(id='page-content'),
    html.Div(struct_layout)
    ])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if not pathname or len(pathname) <= 1:
        raise PreventUpdate
    elif pathname == '/search':
        return html.Div(SearchApp.serve_layout())
    else:
        return html.Div(children=[
            html.Div(struct_component.all_layouts["struct"],
                     style={'width': '500px', 'height': '500px'}),
            DataApp.serve_layout(pathname)
        ])


# This is a work-around hack to show/hide the viewer appropriately.
@app.callback(Output('visualizer', 'style'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if not pathname or len(pathname) <= 1:
        raise PreventUpdate
    elif pathname == '/search':
        return {"display": "none"}
    else:
        return {"display": "block"}


# This is to update the viewer with the appropriate material.
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

