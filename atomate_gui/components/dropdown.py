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

    def create_callback(self, values, manager, html, dcc):
        components = manager.components
        active_fields = []

        for component in components:
            if component.mongo_name in values:
                active_fields.append(component.name)

        manager.update_activity(active_fields)

        return manager.generate_components(html, dcc)

    def generate_component(self, dcc, ids):
        return dcc.Dropdown(
            id=ids["component_dropdown_id"],
            options=self.options,
            multi=True,
            value="",
            placeholder="Select query fields...",
        )
