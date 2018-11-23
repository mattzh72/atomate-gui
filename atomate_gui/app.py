from layouts.table import serve_layout
from managers.component_manager import ComponentManager
from managers.callback_manager import CallbackManager
import dash
from pymongo import MongoClient
import dash_core_components as dcc
import dash_html_components as html

# Global ID HTML values
ids = {
    "query_input_id": "query-input",
    "fields_input_id": "field_input",
    "textarea_output_id": "textarea_output",
    "table_output_id": "table_output"
}

client = MongoClient()
db = client['thermoelectrics']
collection = db['materials']

queries = ['nelements', 'bandgap']
# fields = ["chemsys"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

component_manager = ComponentManager()
component_manager.add_components(queries, collection, active=True)
html_components = component_manager.generate_components(html, dcc)

app.layout = serve_layout(html_components, html, dcc, ids)
app.config['suppress_callback_exceptions'] = True

callback_manager = CallbackManager()
callback_manager.generate_output_io(component_manager.components)
callback_manager.generate_query_io(component_manager.components, ids["query_input_id"])
callback_manager.generate_table_io(collection, html, ids)
callback_manager.attach_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
