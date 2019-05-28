from atomate_gui.components.slider import Slider
from atomate_gui.components.textarea import TextArea
from atomate_gui.components.dropdown import ComponentDropdown
from atomate_gui.components.checkbox import Checkbox
from dash.dependencies import Input, Output
from atomate_gui.app import app, collection
from atomate_gui.components.table import CollectionTable


class ComponentManager:
    def __init__(self):
        self.components = {}
        self.query_dd = ComponentDropdown()
        self.field_dd = ComponentDropdown()
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
                component = Checkbox(name)

            if item['type'] == str:
                component = TextArea(name)

            if component:
                self.components[name] = component
                self.query_dd.add(component)
                self.field_dd.add(component)

    def get_queries(self):
        queries = {'$and': []}
        if self.active_components.values():
            for component in self.active_components.values():
                if not component.value == component.default:
                    queries['$and'].append(component.get_query())

        if queries['$and']:
            return queries
        else:
            return {'_id': {'$exists': 'true'}}

    def get_fields(self, values, static_value="['material_id']"):
        fields = {'_id': 0}

        if static_value not in values:
            values.append(static_value)

        for val in values:
            fields[self.components[val].mongo] = 1

        return fields

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

    def attach_callbacks(self):
        for name in self.components.keys():
            app.callback(
                Output(name + '-label', 'children'),
                [Input(name, 'id'), Input(name, 'value'), Input(name, 'values')]
            )(lambda ids, value, values: self.cache_component(ids, value if value else values))

        app.callback(
            Output('components-container', 'children'),
            [Input('query-dropdown', 'value')]
        )(lambda values: self.update(values))

        app.callback(
            Output('search-table', 'data'),
            [Input('field-dropdown', 'value'), Input('search-button', 'n_clicks_timestamp')]
        )(lambda values, search_time: CollectionTable.update_data(
            collection.find(self.get_queries(), self.get_fields(values))))

        app.callback(
            Output('search-table', 'columns'),
            [Input('field-dropdown', 'value'), Input('search-button', 'n_clicks_timestamp')]
        )(lambda values, search_time: CollectionTable.update_cols(self.get_fields(values)))










