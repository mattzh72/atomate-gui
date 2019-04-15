from dash.dependencies import Input, Output
from app import ids


class CallbackManager:
    def __init__(self, app, component_manager, query_manager):
        self.ios = []
        self.c_manager = component_manager
        self.q_manager = query_manager
        self.app = app

    def attach_callbacks(self):
        for c_name in self.c_manager.components.keys():
            self.generate_label_io(c_name)

        self.generate_dd_io()
        self.generate_table_io()
        self.generate_btn_io()

        for callback_data in self.ios:
            self.app.callback(
                callback_data["output"],
                callback_data["inputs"]
            )(callback_data["func"])

    def generate_btn_io(self):
        self.ios.append({
            "output": Output(ids["query_input"], 'value'),
            "inputs": [Input(ids["btn"], 'n_clicks')],
            "func": lambda n1: self.c_manager.merge_queries(),
        })

        self.ios.append({
            "output": Output('table-page-index', 'children'),
            "inputs": [Input(ids["table_output"], 'children')],
            "func": lambda children: self.q_manager.create_message(),
        })

    def generate_label_io(self, c_name):
        self.ios.append({
            "output": Output(c_name+'-label', 'children'),
            "inputs": [Input(c_name, 'id'), Input(c_name, 'value')],
            "func": lambda name, val: self.c_manager.cache_component(name, val),
        })

    def generate_table_io(self):
        self.ios.append({
            "output": Output(ids["table_output"], 'children'),
            "inputs": [Input(ids["query_input"], 'value'),
                       Input(ids["fields_input"], 'value'),
                       Input('table-row-dropdown', 'value'),
                       Input('table-forward', 'n_clicks_timestamp'),
                       Input('table-backward', 'n_clicks_timestamp'),
                       Input(ids["btn"], 'n_clicks_timestamp')],
            "func": lambda query, fields, rpp, forward_time, backward_time, search_time: self.q_manager.create_table(query, fields, rpp, forward_time, backward_time, search_time),
        })

    def generate_dd_io(self):
        self.ios.append({
            "output": Output(ids["components"], 'children'),
            "inputs": [Input(ids["query_dropdown"], 'value')],
            "func": lambda values: self.c_manager.update(values),
        })

        self.ios.append({
            "output": Output(ids["fields_input"], 'value'),
            "inputs": [Input(ids["field_dropdown"], 'value')],
            "func": lambda values: self.c_manager.specify_fields(values),
        })


