from dash.dependencies import Input, Output
from components.table import CollectionTable
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

    def generate_output_io(self, components):
        for component in components:
            self.io[component.name] = {
                "output": Output(component.name+'-output-container', 'children'),
                "inputs": [Input(component.name, 'id'), Input(component.name, 'value')],
                "func": lambda name, val: component.generate_query(name, val),
            }

    def generate_query_io(self, components, query_input_id):
        inputs = []
        for component in components:
            inputs.append(Input(component.name+'-output-container', 'children'))

        self.io[query_input_id] = {
            "output": Output(query_input_id, 'value'),
            "inputs": inputs,
            "func": lambda *args: "{{ '$and': {0} }}".format([ast.literal_eval(arg) for arg in args]),
        }

    def generate_table_io(self, collection, html, ids):
        table = CollectionTable()
        self.io["data-table"] = {
            "output": Output(ids["table_output_id"], 'children'),
            "inputs": [Input(ids["query_input_id"], 'value'), Input(ids["fields_input_id"], 'value')],
            "func": lambda query, fields: table.create_callback(query, fields, collection, html),
        }
