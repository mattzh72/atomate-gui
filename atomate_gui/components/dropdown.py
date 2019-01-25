import dash_core_components as dcc
import dash_html_components as html

from app import ids


class ComponentDropdown:
    def __init__(self):
        self.options = []

    def add_options(self, components):
        for component in components:
            self.options.append({
                'label': component.mongo_name, 'value': component.name
            })

    def clear_options(self):
        self.options = []

    def create_callback(self, values, manager):
        components = manager.components
        active_fields = []

        for component in components:
            if component.name in values:
                active_fields.append(component.name)

        manager.update_activity(active_fields)

        return manager.generate_components()

    def create_callback_WIP(self, values, name):
        display = 'none'
        if name in values:
            display = 'block'

        return {
                'display': display,
                'width': '80%',
                'margin-left': '10%',
                'margin-top': '10px',
                'margin-bottom': '10px',
            }

    def generate_component(self):
        return dcc.Dropdown(
            id=ids["component_dropdown"],
            options=self.options,
            multi=True,
            value="",
            placeholder="Select query fields...",
        )
