from components.base import BaseComponent


class Input(BaseComponent):
    type = 'input'

    def __init__(self, name):
        BaseComponent.__init__(self, name)
        self.placeholder = "Input for " + self.name
        self.query_template = "{{ '{0}': '{1}' }}"

    def generate_component(self, html, dcc):
        return html.Div(
            children=[dcc.Input(
                id=self.name,
                className=self.class_name,
                placeholder='Enter a value for ' + self.name,
                type='text',
                value=self.placeholder
            ),
                html.Div(
                    id=self.output_div_name
                )
            ]
        )

    def generate_query(self, name, val):
        assert type(val) is str, "value is not a list:{0}".format(val)

        return self.query_template.format(name, val)
