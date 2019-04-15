import dash
from pymongo import MongoClient

# Global ID HTML values
ids = {
    "query_input": "q-i",
    "fields_input": "f-i",
    "textarea_output": "ta-o",
    "table_output": "t-o",
    "components": "c-c",
    "query_dropdown": "d-q",
    "field_dropdown": "d-f",
    "btn": "s-b",
}

external_stylesheets = ['https://codepen.io/mattzh1314/pen/LajLog.css']

app = dash.Dash(__name__)
server = app.server
app.config['suppress_callback_exceptions'] = True

client = MongoClient()
db = client['thermoelectrics']
collection = db['materials']
