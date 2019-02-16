from components.base import BaseComponent
import dash_core_components as dcc
import dash_html_components as html
import math


class Slider(BaseComponent):
    type = 'slider'

    def __init__(self, name, min_val=0, max_val=10, step=1):
        BaseComponent.__init__(self, name, [min_val, max_val], [min_val, max_val])
        self.min = min_val
        self.max = max_val
        self.step = step
        self.marks = {}

    def auto_scale(self, collection):
        self.auto_scale_range(collection)
        self.auto_scale_step(collection)
        self.auto_generate_marks()

    def auto_generate_marks(self):
        range, mark_step = self.max - self.min, 0

        if range < 10:
            mark_step = 1
        elif range > 10 and range < 50:
            mark_step = 5
        else:
            mark_step = pow(10, math.floor(math.log10(range)))

        mark = self.min

        while mark <= self.max:
            self.marks[mark] = round(mark, 4)
            mark += mark_step

    def auto_scale_step(self, collection):
        sample_field = eval("collection.find_one()" + self.name)
        if isinstance(sample_field, float):
            self.step = (self.max - self.min) / 100
        else:
            self.step = 1

    def generate_component(self):
        return html.Div(
            children=[dcc.RangeSlider(
                id=self.name,
                className=self.class_name,
                count=1,
                min=self.min,
                max=self.max,
                step=self.step,
                value=self.value,
                marks=self.marks,
            ),
                html.Div(
                    id=self.output_div_name,
                    style={
                        'margin-top': '20px',
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
            'type': Slider.type,
            'name': self.name,
            'min_val': self.min,
            'max_val': self.max,
            'step': self.step,
            'marks': self.marks
        })



