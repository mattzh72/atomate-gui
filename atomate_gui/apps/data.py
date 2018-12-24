from app import app, collection
from components.table import CollectionTable

from app import collection

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
        query = {'chemsys': pathname[1:]}
        fields = {'_id':0}
        entry = collection.find(query, fields)[0]

        display_fields = {
            "spacegroup #": entry['spacegroup']['number'],
        }

        return detail_table.generate_details_table(display_fields)
