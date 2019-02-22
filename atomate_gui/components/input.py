from components.base import BaseComponent
import dash_core_components as dcc
import dash_html_components as html


class Input(BaseComponent):
    type = 'input'

    def __init__(self, name):
        BaseComponent.__init__(self, name, "", "")
        self.placeholder = 'Enter a value for ' + self.name

    def get_query(self):
        return {self.mongo: {'$regex': '.*' + self.value + '.*'}}

    def generate_component(self):
        children = [
            self.generate_label_div(),
            html.Div(
                children=[dcc.Input(
                    id=self.name,
                    placeholder=self.placeholder,
                    type='text',
                    value=self.value,
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
            'type': Input.type,
            'name': self.name
        })

