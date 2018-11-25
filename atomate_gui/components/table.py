import ast
import pandas as pd


class CollectionTable:
    def __init__(self):
        self.data_frame = None

    def create_callback(self, query, fields, collection, html):
        try:
            self.query_data(collection, query, fields)
            return [self.generate_table(html)]
        except Exception:
            return "Not a valid query."

    def query_data(self, collection, query, fields, row_label="chemsys"):
        mat_structs = {}

        for post in collection.find(ast.literal_eval(query), ast.literal_eval(fields)):
            mat_structs[post[row_label]] = post

        for mat in mat_structs:
            for features in mat_structs[mat]:
                if isinstance(mat_structs[mat][features], dict):
                    mat_structs[mat][features] = str(mat_structs[mat][features])

        self.data_frame = pd.DataFrame.from_dict(mat_structs, orient='index')

    def generate_table(self, html, max_rows=20):
        return html.Table(
            # Header
            [html.Tr([html.Th(col) for col in self.data_frame.columns])] +

            # Body
            [html.Tr([
                html.Td(self.data_frame.iloc[i][col]) for col in self.data_frame.columns
            ]) for i in range(min(len(self.data_frame), max_rows))],

            style={
                'width': '50%',
                'margin-bottom': '20px',
                'text-align': 'center',
                'margin-left': '25%'
            }
        )



