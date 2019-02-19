import dash_html_components as html

class BaseComponent:
    type = 'base'
    query = "{{ '{0}': {{ '$exists': 'true' }} }}"

    def __init__(self, name, value, default=None):
        self.name = name
        self.value = value
        self.default = default

        self.class_name = self.name + "-" + self.type
        self.mongo_name = name.replace("']['", ".").replace("['", "").replace("']", "")
        self.label = self.name + '-label'
        self.output = self.name + '-output'
        self.parent_name = self.name + '-parent-container'

    def get_query(self):
        return BaseComponent.query.format(self.name)

    def generate_label_div(self):
        return html.Div(
            id=self.label,
            style={
                'margin-top': '20px',
                'margin-bottom': '10px',
                'font-size': '10px',
            }
        )

    def generate_output_div(self, children=None):
        return html.Div(
            id=self.output,
            children=children,
            style={
                'display': 'None'
            }
        )



