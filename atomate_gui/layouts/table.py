def serve_layout(manager, html, dcc, ids):
    children = [
        html.Div(
            children='Control Suite',
            style={
                'width': '100%',
                'margin-bottom': '10px',
                'margin-top': '10px',
                'text-align': 'center'
            }
        ),
        html.Div(
            children=[manager.dropdown.generate_component(dcc, ids)],
            style={
                'width': '80%',
                'margin-left': '10%',
                'margin-bottom': '10px',
                'margin-top': '10px',
            }
        ),
        html.Div(
            id=ids["component-container_id"],
            children=[],
            style={
                'width': '80%',
                'margin-left': '10%',
                'border': '1px solid #D3D3D3',
                "border-radius": "5px",
                'margin-bottom': '20px',
                'padding-top': '10px',
            }
        ),
    ]

    return html.Div(children=[
        html.H1(
            children='Materialize Search Engine',
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

        html.Div(
            id='query_components',
            children=children,
            style={
                'width': '50%',
                'margin-left': '25%',
                'margin-bottom': '20px',
                'text-align': 'center',
                'border': '1px solid #D3D3D3',
                "border-radius": "5px",
            }
        ),

        dcc.Input(
            id=ids["query_input_id"],
            placeholder='Put a query here...',
            type='text',
            value="{'nelements': {'$gte': 6, '$lte': 8}}",
            style={
                'width': '60%',
                'margin-bottom': '10px',
                'margin-left': '20%'
            },
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


