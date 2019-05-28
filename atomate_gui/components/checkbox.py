from atomate_gui.components.base import BaseComponent
import dash_core_components as dcc
import dash_html_components as html


class Checkbox(BaseComponent):
    type = 'checkbox'

    def __init__(self, name):
        BaseComponent.__init__(self, name, [True, False], [True, False])

    def get_query(self):
        if len(self.value) in (2, 0):
            return self.get_base_query()
        if len(self.value) == 1:
            return {self.mongo: self.value[0]}
        else:
            raise RuntimeError("More than three values in values for checkbox: " + self.mongo)

    def generate_component(self):
        children = html.Div(
            children=[
                self.generate_label_div(),
                dcc.Checklist(
                    id=self.name,
                    options=[
                        {'label': 'True', 'value': True},
                        {'label': 'False', 'value': False},
                    ],
                    values=[True, False]
                )],
            id=self.parent,
            className='checkbox-component',
        )

        return self.generate_wrapper(children)

    def get_label(self):
        return '{0} is {1}'.format(self.mongo, ', '.join(map(str, self.value)))

    def __str__(self):
        return str({
            'type': Checkbox.type,
            'name': self.name,
        })



