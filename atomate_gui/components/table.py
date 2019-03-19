import ast
import pandas as pd
import dash_html_components as html
from app import collection
import collections


class CollectionTable:
    def __init__(self):
        self.data_frame = None

    def create_callback(self, query, fields):
        try:
            self.query_data(query, fields)
            return [self.generate_search_table()]
        except Exception:
            return "Not a valid query."

    def query_data(self, query, fields, row_label="chemsys", unravel=True):
        mat_structs = {}
        nested = False

        #check for nested elements
        if unravel:
            post = collection.find_one(ast.literal_eval(query), ast.literal_eval(fields))
            for k, v in post.items():
                if isinstance(v, dict):
                    nested = True

        for post in collection.find(ast.literal_eval(query), ast.literal_eval(fields)):
            mat_structs[post[row_label]] = post

        if nested and unravel:
            for mat in mat_structs:
                mat_structs[mat] = self.flatten(mat_structs[mat])

        for mat in mat_structs:
            for feature in mat_structs[mat]:
                mat_structs[mat][feature] = str(mat_structs[mat][feature])

        self.data_frame = pd.DataFrame.from_dict(mat_structs, orient='index')

    def flatten(self, d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def generate_search_table(self, max_rows=20):
        row_range = range(min(len(self.data_frame), max_rows))

        header = [html.Tr([html.Th("")] + [html.Th(col) for col in self.data_frame.columns])]
        body = [html.Tr(
            [html.Td(html.A("View", href="/{0}".format(self.data_frame.iloc[i]['material_id']), target='_blank'))] +
            [html.Td(self.data_frame.iloc[i][col]) for col in self.data_frame.columns]) for i in row_range]

        table_output = header + body

        return html.Table(
            table_output,
            style={
                'width': '90%',
                'margin-left': '5%',
                'margin-top': '10px',
                'height': '80%',
                'text-align': 'center',
            }
        )

    def generate_details_table(self, fields_dict):
        table_output = []

        for k, v in fields_dict.items():
            table_output += [html.Tr([html.Td(str(k)), html.Td(str(v))])]

        return html.Table(
            table_output,
            style={
                'width': '50%',
                'margin-bottom': '20px',
                'text-align': 'center',
                'margin-left': '25%',
            }
        )



