import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import crystal_toolkit as ct
from pymatgen import Structure, Lattice

from app import app, collection
from apps import search, data

# example_struct = Structure.from_spacegroup(
#     "P6_3mc",
#     Lattice.hexagonal(3.22, 5.24),
#     ["Ga", "N"],
#     [[1 / 3, 2 / 3, 0], [1 / 3, 2 / 3, 3 / 8]],
# )

ct.register_app(app)
struct_component = ct.StructureMoleculeComponent(None)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/search':
        return search.layout()
    else:
        # return data.layout(pathname)
        material_id = pathname[1:]
        query = {'material_id': material_id}
        entries = collection.find(query)

        data = ct.MPComponent.to_data(Structure.from_dict(entries[0]["structure"]))
        struct_component.from_data(data)
        return html.Div([
            ct.MPComponent.all_app_stores(),
            struct_component.standard_layout,
        ])
        # return html.Div([
        #     html.Div(children=[
        #         ct.MPComponent.all_app_stores(),
        #         struct_component.standard_layout
        #     ],
        #         style={
        #             'height': '30%',
        #     }),
        #     data.layout(pathname)
        # ])



if __name__ == '__main__':
    app.run_server(debug=True)

