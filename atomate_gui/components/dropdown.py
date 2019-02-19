import dash_core_components as dcc
import dash_html_components as html

from app import ids


class ComponentDropdown:
    def __init__(self):
        self.options = []
        self.values = [
            "['nelements']",
            # "['material_id']",
            # "['spacegroup']['number']",
            # "['stability']['e_above_hull']",
            # "['bandstructure']['is_gap_direct']",
            # "['chemsys']"
        ]

    def add_options(self, components):
        for component in components.values():
            self.options.append({
                'label': component.mongo_name, 'value': component.name
            })

    def clear_options(self):
        self.options = []

    @staticmethod
    def create_callback(self, vals, c_manager):
        for name in list(c_manager.active_components.keys()):
            if name not in vals:
                c_manager.deactivate_component(name)

        for val in vals:
            if val not in list(c_manager.active_components.keys()):
                c_manager.activate_component(val)

        return c_manager.generate_active_components()

    def generate_component(self):
        return dcc.Dropdown(
            id=ids["dropdown"],
            options=self.options,
            multi=True,
            value=self.values,
            placeholder="Select query fields...",
        )
