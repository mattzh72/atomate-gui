from dash.dependencies import Input, Output
from components.table import CollectionTable
from managers.query_manager import QueryManager
import ast

class CallbackManager:
    def __init__(self):
        self.io = {}

    def attach_callbacks(self, app):
        for callback_data in list(self.io.values()):
            app.callback(
                callback_data["output"],
                callback_data["inputs"]
            )(callback_data["func"])

    def generate_all_io(self, manager, collection, html, dcc, ids):
        self.generate_output_io(manager.components)
        self.generate_dropdown_io(manager, html, dcc, ids)
        self.generate_query_io(manager.components, ids)
        self.generate_table_io(collection, html, ids)

    def generate_output_io(self, components):
        for component in components:
            self.io[component.name] = {
                "output": Output(component.name+'-output-container', 'children'),
                "inputs": [Input(component.name, 'id'), Input(component.name, 'value')],
                "func": lambda name, val: component.generate_query(name, val),
            }

    def generate_query_io(self, components, ids):
        inputs = []
        # inputs = [Input(ids["component-container_id"], 'children')]
        for component in components:
            inputs.append(Input(component.name+'-output-container', 'children'))
        # query_manager = QueryManager()

        self.io[ids["query_input_id"]] = {
            "output": Output(ids["query_input_id"], 'value'),
            "inputs": inputs,
            # "func": lambda children: query_manager.create_query(children),
            "func": lambda *args: "{{ '$and': {0} }}".format([ast.literal_eval(arg) for arg in [a for a in args if a != "@HIDDEN"]])
        }

    def generate_table_io(self, collection, html, ids):
        table = CollectionTable()
        self.io["data-table"] = {
            "output": Output(ids["table_output_id"], 'children'),
            "inputs": [Input(ids["query_input_id"], 'value'), Input(ids["fields_input_id"], 'value')],
            "func": lambda query, fields: table.create_callback(query, fields, collection, html),
        }

    def generate_dropdown_io(self, manager, html, dcc, ids):
        self.io["component_dropdown"] = {
            "output": Output(ids["component-container_id"], 'children'),
            "inputs": [Input(ids["component_dropdown_id"], 'value')],
            "func": lambda values: manager.dropdown.create_callback(values, manager, html, dcc),
        }
