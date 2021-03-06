import dash
from pymongo import MongoClient

# Global ID HTML values
ids = {
    "query_input": "q-i",
    "fields_input": "f-i",
    "textarea_output": "ta-o",
    "table_output": "search-table-wrapper",
    "components": "components-container",
    "query_dropdown": "query-dropdown",
    "field_dropdown": "field-dropdown",
    "btn": "search-button",
}

app = dash.Dash(__name__)
server = app.server
app.config['suppress_callback_exceptions'] = True

client = MongoClient()
db = client['thermoelectrics']
collection = db['materials']
