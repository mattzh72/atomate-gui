from dash.dependencies import Input, Output
from components.table import CollectionTable
from managers.query_manager import QueryManager
from app import ids


class CallbackManager:
    def __init__(self, app, component_manager):
        self.ios = []
        self.c_manager = component_manager
        self.app = app

    def attach_callbacks(self):
        self.generate_output_io()
        self.generate_dd_io()
        # self.generate_query_io()
        self.generate_table_io()

        for callback_data in self.ios:
            self.app.callback(
                callback_data["output"],
                callback_data["inputs"]
            )(callback_data["func"])

    def generate_output_io(self):
        for c_name in self.c_manager.components.keys():
            self.ios.append({
                "output": Output(c_name+'-label', 'children'),
                "inputs": [Input(c_name, 'id'), Input(c_name, 'value')],
                "func": lambda name, val: self.c_manager.cache_component(name, val),
            })

    def generate_query_io(self):
        print("printing queries")
        inputs = []

        for c_name in self.c_manager.components.keys():
            inputs.append(Input(c_name, 'id'))
            inputs.append(Input(c_name, 'value'))

        self.ios.append({
            "output": Output(ids["query_input"], 'value'),
            "inputs": inputs,
            "func": lambda *args: QueryManager().create_query(args[::2], args[1::2])
        })

    def generate_table_io(self):
        self.ios.append({
            "output": Output(ids["table_output"], 'children'),
            "inputs": [Input(ids["query_input"], 'value'), Input(ids["fields_input"], 'value')],
            "func": lambda query, fields: CollectionTable().create_callback(query, fields),
        })

    def generate_dd_io(self):
        self.ios.append({
            "output": Output(ids["components"], 'children'),
            "inputs": [Input(ids["dropdown"], 'value')],
            "func": lambda values: self.c_manager.dropdown.create_callback(values, self.c_manager),
        })
