from components.base import BaseComponent
import dash_core_components as dcc
import dash_html_components as html


class Input(BaseComponent):
    type = 'input'

    def __init__(self, name):
        BaseComponent.__init__(self, name, "", "")
        self.placeholder = 'Enter a value for ' + self.name

    def generate_component(self):
        return html.Div(
            children=[dcc.Input(
                id=self.name,
                className=self.class_name,
                placeholder=self.placeholder,
                type='text',
                value=self.value,
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
            'type': Input.type,
            'name': self.name
        })

