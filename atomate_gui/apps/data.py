from app import app, collection
from components.table import CollectionTable

"""
spacegroup.number, 
spacegroup.crystal_system, 
len(structure.sites) (???),
density (???), 
structure.lattice.volume, 
stability.e_above_hull, 
stability.decomposes_to[0].formula, 
bandstructure.bandgap, 
bandstructure.is_gap_direct, 
bandstructure.is_metal
"""

def layout(pathname):
    if pathname:
        detail_table = CollectionTable()
        query = {'material_id': pathname[1:]}
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
