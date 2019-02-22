import dash_core_components as dcc


class ComponentDropdown:
    def __init__(self):
        self.options = []

    def add(self, component):
        self.options.append({
            'label': component.mongo, 'value': component.name
        })

    def clear_options(self):
        self.options = []

    def generate_component(self, name, values):
        return dcc.Dropdown(
            id=name,
            options=self.options,
            multi=True,
            value=values,
            placeholder="Select query fields...",
        )
