from components.slider import Slider
from components.input import Input
from components.dropdown import ComponentDropdown
from components.radio import RadioBoolean


class ComponentManager:
    def __init__(self):
        self.components = {}
        self.query_dropdown = ComponentDropdown()
        self.field_dropdown = ComponentDropdown()
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
                component = RadioBoolean(name)

            if item['type'] == str:
                component = Input(name)

            if component:
                self.components[name] = component
                self.query_dropdown.add(component)
                self.field_dropdown.add(component)

    def merge_queries(self):
        queries = []

        for component in self.active_components.values():
            if not component.value == component.default:
                queries.append(component.get_query())

        if queries:
            return "{{ '$and': {0} }}".format(queries)
        else:
            return "{ '_id': { '$exists': 'true' } }"

    def specify_fields(self, values):
        fields = {'_id': 0}

        for val in values:
            fields[self.components[val].mongo] = 1

        return str(fields)

    def update(self, values):
        for name in list(self.active_components.keys()):
            if name not in values:
                self.deactivate_component(name)

        for val in values:
            if val not in list(self.active_components.keys()):
                self.activate_component(val)

        return self.generate_active_components()

    def activate_component(self, name):
        self.active_components[name] = self.components[name]

    def deactivate_component(self, name):
        self.active_components.pop(name)
        self.clear_cache(name)

    def cache_component(self, name, value):
        self.components[name].value = value

        return self.components[name].get_label()

    def clear_cache(self, name):
        if self.components[name].default:
            self.components[name].value = self.components[name].default

    def generate_active_components(self):
        children = []
        for component in self.active_components.values():
            if component:
                children.append(component.generate_component())

        return children









