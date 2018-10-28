from pprint import pformat
import dash_core_components as dcc
import dash_html_components as html


def return_posts(collection):
    text = []
    for post in collection.find():
        text += [pformat(post)]

    return text


def generate_table(data_frame, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in data_frame.columns])] +

        # Body
        [html.Tr([
            html.Td(data_frame.iloc[i][col]) for col in data_frame.columns
        ]) for i in range(min(len(data_frame), max_rows))],

        style={
            'width': '50%',
            'margin-bottom': '20px',
            'text-align': 'center',
            'margin-left': '25%'
            }
    )


def detect_range(field_name, collection):
    max_val, min_val= float('-inf'), float('inf')

    for post in collection.find():
        val = post[field_name]

        if val > max_val:
            max_val = val

        if val < min_val:
            min_val = val

    return min_val, max_val


def choose_component(field_name, collection): #instanceof
    field_type = type(collection.find_one()[field_name])

    if isinstance(field_type, int) or isinstance(field_type, float):
        min_val, max_val = detect_range(field_name, collection)
        step_val = 1

        if isinstance(field_type, float):
            step_val = (max_val - min_val)/100

        return html.Div(
                    children=[dcc.RangeSlider(
                            id=field_name + "-range-slider",
                            count=1,
                            min=min_val,
                            max=max_val,
                            step=step_val,
                            value=[min_val, max_val]
                            ),
                            html.Div(
                                id=field_name + '-output-container-range-slider'
                                )
                            ]
                        )
    elif field_type is str:
        return html.Div(
                    children=[dcc.Input(
                            id=field_name + "-input",
                            placeholder='Enter a value for ' + field_name,
                            type='text',
                            value=''
                            ),
                            html.Div(
                                id=field_name + '-output-container-input'
                                )
                            ]
                        )


def insert_components(queries, fields, collection):
    children_list = []
    for query in queries:
        children_list.append(choose_component(query, collection))

    for field in fields:
        children_list.append(choose_component(field, collection))

    return html.Div(
            id='query_components',
            children=children_list,
            style={
                'width': '50%',
                'margin-bottom': '20px',
                'text-align': 'center',
                }
            )


def insert_components(queries, fields, collection):
    children_list = []
    for query in queries:
        children_list.append(choose_component(query, collection))

    for field in fields:
        children_list.append(choose_component(field, collection))

    return html.Div(
            id='query_components',
            children = children_list,
            style={
                'width': '50%',
                'margin-bottom': '20px',
                'text-align': 'center',
                }
            )
