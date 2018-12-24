import dash
from pymongo import MongoClient

# Global ID HTML values
ids = {
    "query_input": "query-input",
    "fields_input": "field_input",
    "textarea_output": "textarea_output",
    "table_output": "table-output",
    "component_container": "component-container",
    "component_dropdown": "component-dropdown",
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions'] = True

client = MongoClient()
db = client['thermoelectrics']
collection = db['materials']
