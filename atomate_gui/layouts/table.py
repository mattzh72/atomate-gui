ROW_LABEL = "chemsys"


def serve_layout(components, html, dcc, ids):
    return html.Div(children=[
        html.H1(
            children='Materials DB Web UI',
            style={
                'width': '100%',
                'margin-bottom': '10px',
                'margin-top': '20px',
                'text-align': 'center'}
            ),

        html.Div(
            children='This application queries the materials database.',
            style={
                'width': '100%',
                'margin-bottom': '20px',
                'text-align': 'center'
                }
            ),

        components,

        dcc.Input(
            id=ids["query_input_id"],
            placeholder='Put a query here...',
            type='text',
            value="{'nelements': {'$gte': 6, '$lte': 8}}",
            style={
                'width': '60%',
                'margin-bottom': '10px',
                'margin-left': '20%'},
        ),

        dcc.Input(
            id=ids["fields_input_id"],
            placeholder='Put the fields you want to display here...',
            type='text',
            value="{'bandgap': 1, 'chemsys': 1, 'bandstructure': 1, '_id': 0}", #
            style={
                'width': '60%',
                'margin-bottom': '20px',
                'margin-left': '20%'
                },
        ),

        html.Div(
            id=ids["table_output_id"],
            children='No table yet.',
            )
    ])


