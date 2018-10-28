from atomate_gui.layouts.table import serve_layout
import dash
from pymongo import MongoClient

client = MongoClient()
db = client['thermoelectrics']
collection = db['materials']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)
