from atomate_gui.components.base import BaseComponent
import dash_core_components as dcc
import dash_html_components as html


class TextArea(BaseComponent):
    type = 'input'

    def __init__(self, name):
        BaseComponent.__init__(self, name, "", "")
        self.placeholder = 'Enter a value for ' + self.name

    def get_query(self):
        return {self.mongo: {'$regex': '.*' + self.value + '.*'}} if self.value else self.get_base_query()

    def generate_component(self):
        children = html.Div(
                children=[
                    self.generate_label_div(),
                    dcc.Input(
                        id=self.name,
                        placeholder=self.placeholder,
                        type='text',
                        value=self.value,
                    )],
                id=self.parent,
                className='input-component'
            )

        return self.generate_wrapper(children)

    def get_label(self):
        return '{0} is {1}'.format(self.mongo, self.value if self.value else '')

    def __str__(self):
        return str({
            'type': TextArea.type,
            'name': self.name
        })

