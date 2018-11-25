from layouts.table import serve_layout
from managers.component_manager import ComponentManager
from managers.callback_manager import CallbackManager
from managers.collection_manager import CollectionManager

import dash
from pymongo import MongoClient
import dash_core_components as dcc
import dash_html_components as html

# Global ID HTML values
ids = {
    "query_input_id": "query-input",
    "fields_input_id": "field_input",
    "textarea_output_id": "textarea_output",
    "table_output_id": "table-output",
    "component-container_id": "component-container",
    "component_dropdown_id":"component-dropdown",
}

client = MongoClient()
db = client['thermoelectrics']
collection = db['materials']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

sample_entry = {
    'nelements': 4,
    'chemsys': 'Al-Ca-O-S',
    'bandstructure': {
        'bandgap': 4.5088,
        'cbm': 5.2115,
        'vbm': 0.7027,
    }
}

collection_manager = CollectionManager(collection)
# collection_manager.get_metadata()
# print(collection_manager.metadata)

component_manager = ComponentManager()
component_manager.add_components(collection_manager)

app.layout = serve_layout(component_manager, html, dcc, ids)
app.config['suppress_callback_exceptions'] = True

callback_manager = CallbackManager()
callback_manager.generate_all_io(component_manager, collection, html, dcc, ids)
callback_manager.attach_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
