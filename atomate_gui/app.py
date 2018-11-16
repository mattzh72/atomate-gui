from layouts.table import serve_layout
from data import generate_callbacks, generate_all_callbacks
import dash
from pymongo import MongoClient


client = MongoClient()
db = client['thermoelectrics']
collection = db['materials']

queries = ["nelements", 'bandgap']
fields = ["chemsys"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = serve_layout(queries, collection)
app.config['suppress_callback_exceptions'] = True

generate_callbacks(queries, collection, app)

if __name__ == '__main__':
    app.run_server(debug=True)
