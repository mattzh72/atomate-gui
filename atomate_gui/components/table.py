import dash_html_components as html
import collections


class CollectionTable:
    def __init__(self):
        pass

    @staticmethod
    def update_data(results):
        return [CollectionTable.flatten(x) for x in results]

    @staticmethod
    def update_cols(fields):
        return [{'name': x, 'id': x} for x in fields if x != '_id']

    @staticmethod
    def find_non_alnum_keys(result):
        return [k for k, v in result.items() if not isinstance(v, (float, int, complex, str)) or isinstance(v, bool)]

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



