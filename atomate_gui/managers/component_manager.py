from components.slider import Slider
from components.input import Input
from components.dropdown import ComponentDropdown
import collections


class ComponentManager:
    def __init__(self):
        self.components = []
        self.dropdown = ComponentDropdown()

    def add_components(self, collection_manager):
        collection_manager.set_metadata()

        for data_type, fields in collection_manager.metadata.items():
            for name, value in fields.items():
                component = None

                if data_type == 'nums':
                    component = Slider(name, value[0], value[1])
                    component.auto_scale_step(collection_manager.collection)
                    component.auto_generate_marks()
                elif data_type == 'strings':
                    component = Input(name)

                if component:
                    self.components.append(component)

            self.dropdown.add_options(self.components)

    def update_activity(self, active_fields):
        for component in self.components:
            if component.name in active_fields:
                component.active = True
            else:
                component.active = False

    def report_activity(self):
        activity = []
        for component in self.components:
            activity.append(component.active)

        return activity

    def remove_all_components(self):
        self.components = []

    def generate_components(self, html, dcc):
        html_components = []

        for component in self.components:
            html_components.append(component.generate_component(html, dcc))

        return html_components







