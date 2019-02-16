import dash
from pymongo import MongoClient

# Global ID HTML values
ids = {
    "query_input": "q-i",
    "fields_input": "f-i",
    "textarea_output": "ta-o",
    "table_output": "t-o",
    "components": "c-c",
    "dropdown": "c-d",
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions'] = True

client = MongoClient()
db = client['thermoelectrics']
collection = db['materials']
