from components.base import BaseComponent
import dash_core_components as dcc
import dash_html_components as html


class RadioBoolean(BaseComponent):
    type = 'radio'

    def __init__(self, name):
        BaseComponent.__init__(self, name, False, None)
        self.truthy_val = True
        self.falsey_val = False

    def get_query(self):
        return {self.mongo: self.value}

    def generate_component(self):
        children = [html.Div(
            children=[
                self.generate_label_div(),
                dcc.RadioItems(
                    id=self.name,
                    options=[
                        {'label': 'True', 'value': self.truthy_val},
                        {'label': 'False', 'value': self.falsey_val},
                    ],
                )],
            id=self.parent,
            style={
                'width': '80%',
                'margin-left': '10%'
            }
        )]

        return self.generate_wrapper(children)

    def get_label(self):
        return '{0} is {1}'.format(self.mongo, self.value)

    def __str__(self):
        return str({
            'type': RadioBoolean.type,
            'name': self.name,
            'truth': self.truthy_val,
            'false': self.falsey_val,
        })



