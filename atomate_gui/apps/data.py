from app import app, collection
from components.table import CollectionTable
import crystal_toolkit as ct
import dash_html_components as html
from pymatgen import Structure


def layout(pathname):
    if pathname:
        material_id = pathname[1:]
        query = {'material_id': material_id}
        entry = collection.find(query)[0]

        return html.Div(children=[
            html.H1(
                children="Structure " + material_id,
                style={
                    'width': '100%',
                    'margin-bottom': '10px',
                    'text-align': 'center'}
            ),
            # generate_visual(material_id, entry),
            generate_data_table(entry)
        ])


def generate_visual(material_id, entry):
    ct.register_app(app)
    structure = Structure.from_dict(entry["structure"])
    struct_component = ct.StructureMoleculeComponent(structure, id=material_id)

    return html.Div([
        ct.MPComponent.all_app_stores(),
        struct_component.standard_layout
    ], style={
        'height': '30%'
    })


def generate_data_table(entry):
    detail_table = CollectionTable()

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
