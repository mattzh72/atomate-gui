from app import app, collection
from components.table import CollectionTable
# import crystal_toolkit as ct
import dash_html_components as html
# from pymatgen import Structure, Lattice


def layout(pathname):
    if pathname:
        material_id = pathname[1:]

        return html.Div(children=[
            html.H1(
                children="Structure " + material_id,
                style={
                    'width': '100%',
                    'margin-bottom': '10px',
                    'margin-top': '20px',
                    'text-align': 'center'}
            ),
            # generate_visual(material_id[0] + "p" + material_id[1:]),
            generate_data_table(material_id)
        ])


# def generate_visual(material_id):
#     ct.register_app(app)
#
#     structure = Structure.from_spacegroup(
#         "P6_3mc",
#         Lattice.hexagonal(3.22, 5.24),
#         ["Ga", "N"],
#         [[1 / 3, 2 / 3, 0], [1 / 3, 2 / 3, 3 / 8]],
#     )
#
#     struct_component = ct.StructureMoleculeComponent("mp-100", id=material_id)
#
#     return html.Div([
#         ct.MPComponent.all_app_stores(),
#         struct_component.standard_layout
#     ])

def generate_data_table(material_id):
    detail_table = CollectionTable()
    query = {'material_id': material_id}
    entry = collection.find(query)[0]

    display_fields = {
        "spacegroup #": entry['spacegroup']['number'],
        "crystal system": entry['spacegroup']['crystal_system'],
        "sites": len(entry['structure']['sites']),
        "is metal": entry['bandstructure']['is_metal'],
        "volume:": entry['structure']['lattice']['volume'],
        "e_above_hull": entry['stability']['e_above_hull'],
        "decomposes into": entry['stability']['decomposes_to'],
        "bandgap": entry['bandstructure']['bandgap'],
        "is direct": entry['bandstructure']['is_gap_direct'],
    }

    return detail_table.generate_details_table(display_fields)