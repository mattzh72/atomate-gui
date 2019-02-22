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

    def get_query(self):
        return {self.m_name: {'$exists': 'true'}}

    def generate_label_div(self):
        return html.Div(
            id=self.label,
            style={
                'margin-top': '10px',
                'margin-bottom': '5px',
                'font-size': '12px',
            }
        )

    def generate_wrapper(self, children):
        return html.Div(
            id=self.wrapper,
            children=children,
            style={
                'border': '1px solid #D3D3D3',
                'border-radius': '5px',
                'height': '90px',
                'width': '35%',
                'max-width': '300px',
                'margin': '5px',
                'padding-top': '5px',
                'padding-bottom': '5px',
                'display': 'inline-block'
            }
        )



