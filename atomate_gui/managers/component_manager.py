from components.slider import Slider
from components.input import Input
from components.dropdown import ComponentDropdown
from components.radio import RadioBoolean


class ComponentManager:
    def __init__(self):
        self.components = {}
        self.dropdown = ComponentDropdown()
        self.active_components = {}

    def add_components(self, collection_manager):
        collection_manager.set_metadata()

        for item in collection_manager.metadata:
            component = None
            name = item['name']

            if item['type'] == int:
                component = Slider(name, item['min'], item['max'])
                component.auto_generate_marks()

            if item['type'] == bool:
                component = Input(name)

            if item['type'] == str:
                component = RadioBoolean(name)

            if component:
                self.components[name] = component

        self.dropdown.add_options(self.components)

    def merge_queries(self):
        queries = []

        for component in self.active_components.values():
            queries.append(component.get_query())

        return "{{ '$and': {0} }}".format(queries)

    def generate_hidden_outputs(self):
        children = []

        for component in self.components:
            children.append(component.generate_output_div)

        return children

    def activate_component(self, name):
        self.active_components[name] = self.components[name]

    def deactivate_component(self, name):
        self.active_components.pop(name)
        self.clear_cache(name)

    def cache_component(self, name, value):
        self.components[name].value = value

        return "{0} for {1}".format(value, name)

    def clear_cache(self, name):
        if self.components[name].default:
            self.components[name].value = self.components[name].default

    def generate_active_components(self):
        children = []
        for component in self.active_components.values():
            if component:
                children.append(component.generate_component())

        return children








