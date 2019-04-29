import pandas as pd
import dash_html_components as html
import collections


class CollectionTable:
    def __init__(self):
        pass

    @staticmethod
    def create_data_frame(results, row_label):
        structs = {}
        for result in results:
            mat = {}
            for name, value in result.items():
                if isinstance(value, dict):
                    subname, value = next(iter(value.items()))
                    name = '{}.{}'.format(name, subname)
                mat[name] = str(value)
            structs[mat[row_label]] = mat

        return pd.DataFrame.from_dict(structs, orient='index')

    @staticmethod
    def generate_search_table(results, row_label="material_id"):
        data_frame = CollectionTable.create_data_frame(results, row_label)

        header = [html.Tr([html.Th("")] + [html.Th(col) for col in data_frame.columns])]
        body = [html.Tr(
            [html.Td(html.A("View", href="/{0}".format(data_frame.iloc[i]['material_id']), target='_blank'))] +
            [html.Td(data_frame.iloc[i][col]) for col in data_frame.columns]) for i in range(len(data_frame))]

        table_output = header + body

        return html.Table(
            id='search-table',
            children=table_output,
        )

    @staticmethod
    def flatten(d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(CollectionTable.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def generate_details_table(fields_dict):
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



