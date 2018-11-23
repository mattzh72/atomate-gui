from components.base import BaseComponent


class Slider(BaseComponent):
    type = 'slider'

    def __init__(self, name, min_val=0, max_val=10, step=1):
        BaseComponent.__init__(self, name)
        self.min = min_val
        self.max = max_val
        self.step = step
        self.query_template = "{{'{0}': {{'$gte': {1}, '$lte': {2}}} }}"

    def auto_scale(self, collection):
        self.auto_scale_range(collection)
        self.auto_scale_step(collection)

    def auto_scale_range(self, collection):
        max_val, min_val = float('-inf'), float('inf')

        for post in collection.find():
            val = post[self.name]

            if val > max_val:
                max_val = val

            if val < min_val:
                min_val = val

        self.min = min_val
        self.max = max_val

    def auto_scale_step(self, collection):
        if isinstance(collection.find_one()[self.name], float):
            self.step = (self.max - self.min) / 100
        else:
            self.step = 1

    def generate_component(self, html, dcc):
        return html.Div(
            children=[dcc.RangeSlider(
                id=self.name,
                className=self.class_name,
                count=1,
                min=self.min,
                max=self.max,
                step=self.step,
                value= [self.min, self.max]
            ),
                html.Div(
                    id=self.output_div_name
                )
            ]
        )

    def generate_query(self, name, val):
        assert type(val) is list, "value is not a list:{0}".format(val)

        return self.query_template.format(name, val[0], val[1])


