from components.base import BaseComponent
import dash_core_components as dcc
import dash_html_components as html


class RadioBoolean(BaseComponent):
    type = 'radio'

    def __init__(self, name):
        BaseComponent.__init__(self, name, False, None)
        self.truthy_val = True
        self.falsey_val = False

    def generate_component(self):
        return html.Div(
            children=[dcc.RadioItems(
                id=self.name,
                className=self.class_name,
                options=[
                    {'label': 'True', 'value': self.truthy_val},
                    {'label': 'False', 'value': self.falsey_val},
                ],
            ),
                html.Div(
                    id=self.output_div_name,
                    style={
                        'margin-top': '20px',
                        'margin-bottom': '10px',
                        'font-size': '10px',
                    }
                )
            ],
            id=self.parent_name,
            style={
                'width': '80%',
                'margin-left': '10%',
                'margin-top': '10px',
                'margin-bottom': '10px',
            }
        )

    def __str__(self):
        return str({
            'type': RadioBoolean.type,
            'name': self.name,
            'truth': self.truthy_val,
            'false': self.falsey_val,
        })



