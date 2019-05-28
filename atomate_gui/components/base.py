import dash_html_components as html


class BaseComponent:
    type = 'base'
    query = "{{ '{0}': {{ '$exists': 'true' }} }}"

    def __init__(self, name, value, default=None):
        self.name = name
        self.value = value
        self.default = default

        self.mongo = name.replace("']['", ".").replace("['", "").replace("']", "")
        self.label = self.name + '-label'
        self.output = self.name + '-output'
        self.parent = self.name + '-parent-container'
        self.wrapper = self.name + '-wrapper'

    def get_base_query(self):
        return {self.mongo: {'$exists': 'true'}}

    def generate_label_div(self):
        return html.Div(
            id=self.label,
            className='component-label',
        )

    def generate_wrapper(self, children):
        return html.Div(
            id=self.wrapper,
            className='component',
            children=children,
        )




