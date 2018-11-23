from components.slider import Slider
from components.input import Input


class ComponentManager:
    def __init__(self):
        self.components = []
        self.active_components = []

    def add_components(self, fields, collection, active=False):
        for field in fields:
            sample_entry = collection.find_one()[field]
            component = None

            if isinstance(sample_entry, (int, float)):
                component = Slider(field)
                component.auto_scale(collection)
            elif isinstance(sample_entry, str):
                component = Input(field)

            self.components.append(component)
            if active:
                self.active_components.append(component)

    def generate_components(self, html, dcc):
        children = []

        for component in self.active_components:
            children.append(component.generate_component(html, dcc))

        return html.Div(
            id='query_components',
            children=children,
            style={
                'width': '50%',
                'margin-bottom': '20px',
                'text-align': 'center',
            }
        )
