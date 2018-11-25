from components.base import BaseComponent


class Input(BaseComponent):
    type = 'input'

    def __init__(self, name, active=False):
        BaseComponent.__init__(self, name, active)
        self.placeholder = 'Enter a value for ' + self.name

    def generate_component(self, html, dcc):
        display = 'none'
        if self.active:
            display = 'block'

        return html.Div(
            children=[dcc.Input(
                id=self.name,
                className=self.class_name,
                placeholder=self.placeholder,
                type='text',
                value="",
            ),
                html.Div(
                    id=self.output_div_name,
                    style={
                        'margin-top': '2px',
                        'margin-bottom': '10px',
                        'font-size': '10px',
                    }
                )
            ],
            style={
                'display': display,
                'width': '80%',
                'margin-left': '10%',
                'margin-top': '10px',
                'margin-bottom': '10px',
            }
        )
