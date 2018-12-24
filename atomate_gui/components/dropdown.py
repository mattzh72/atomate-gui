import dash_core_components as dcc
import dash_html_components as html

from app import ids

class ComponentDropdown:
    def __init__(self):
        self.options = []

    def add_options(self, components):
        for component in components:
            self.options.append({
                'label': component.mongo_name, 'value': component.mongo_name
            })

    def clear_options(self):
        self.options = []

    def create_callback(self, values, manager):
        components = manager.components
        active_fields = []

        for component in components:
            if component.mongo_name in values:
                active_fields.append(component.name)

        manager.update_activity(active_fields)

        return manager.generate_components()

    def generate_component(self):
        return dcc.Dropdown(
            id=ids["component_dropdown"],
            options=self.options,
            multi=True,
            value="",
            placeholder="Select query fields...",
        )
