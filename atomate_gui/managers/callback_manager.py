from dash.dependencies import Input, Output
from components.table import CollectionTable
from managers.query_manager import QueryManager
from app import ids


class CallbackManager:
    def __init__(self):
        self.io = {}

    def attach_callbacks(self, app):
        for callback_data in list(self.io.values()):
            app.callback(
                callback_data["output"],
                callback_data["inputs"]
            )(callback_data["func"])

    def generate_all_io(self, manager):
        self.generate_output_io(manager.components)
        self.generate_dropdown_io(manager)
        self.generate_query_io(manager.components)
        self.generate_table_io()

    def generate_output_io(self, components):
        for component in components:
            self.io[component.name] = {
                "output": Output(component.name+'-output-container', 'children'),
                "inputs": [Input(component.name, 'id'), Input(component.name, 'value')],
                "func": lambda name, val: "You selected {0} for {1}".format(val, name),
            }

    def generate_query_io(self, components):
        inputs = []

        for component in components:
            inputs.append(Input(component.name, 'id'))
            inputs.append(Input(component.name, 'value'))
            inputs.append(Input(component.name + '-parent-container', 'style'))
        query_manager = QueryManager()

        self.io[ids["query_input"]] = {
            "output": Output(ids["query_input"], 'value'),
            "inputs": inputs,
            "func": lambda *args: query_manager.create_query(args[::3], args[1::3], args[2::3])
        }

    def generate_table_io(self):
        table = CollectionTable()
        self.io["data-table"] = {
            "output": Output(ids["table_output"], 'children'),
            "inputs": [Input(ids["query_input"], 'value'), Input(ids["fields_input"], 'value')],
            "func": lambda query, fields: table.create_callback(query, fields),
        }

    def generate_dropdown_io(self, manager):
        self.io["component_dropdown"] = {
            "output": Output(ids["component_container"], 'children'),
            "inputs": [Input(ids["component_dropdown"], 'value')],
            "func": lambda values: manager.dropdown.create_callback(values, manager),
        }
