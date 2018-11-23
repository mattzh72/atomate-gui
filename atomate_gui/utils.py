def generate_table(data_frame, html, max_rows=20):
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


