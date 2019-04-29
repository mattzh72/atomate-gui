from components.base import BaseComponent
import dash_core_components as dcc
import dash_html_components as html
from math import floor, log10, ceil


class Slider(BaseComponent):
    type = 'slider'

    def __init__(self, name, min_val=0, max_val=10, step=1):
        BaseComponent.__init__(self, name, [min_val, max_val], [min_val, max_val])
        self.min = min_val
        self.max = max_val
        self.step = step
        self.marks = {}

    def get_query(self):
        return {self.mongo: {'$gte': self.value[0], '$lte': self.value[1]}}

    def auto_scale(self, collection):
        self.auto_scale_range(collection)
        self.auto_scale_step(collection)
        self.auto_generate_marks()

    def auto_generate_marks(self):
        def round_sig(x, sig=3):
            return round(x, sig - int(floor(log10(abs(x)))) - 1)

        diff = self.max - self.min
        lower = self.min
        upper = self.max
        count = 5

        if isinstance(upper, int) and isinstance(lower, int):
            self.step = 1
        else:
            self.step = 0.00001

        if diff > count:
            self.marks[lower] = floor(lower)
            self.marks[upper] = ceil(upper)

            if isinstance(diff, float):
                dist = diff / count
            else:
                dist = max(1, 20 * floor(log10(diff)))
                count = int(round(diff / dist))
        else:
            self.marks[lower] = round_sig(lower)
            self.marks[upper] = round_sig(upper)
            dist = round_sig(diff/count)

        for i in range(1, count):
            val = lower + i * dist
            pretty_val = val

            if isinstance(val, float):
                pretty_val = round_sig(val)

            self.marks[val] = pretty_val

    def auto_scale_step(self, collection):
        sample_field = eval("collection.find_one()" + self.name)
        if isinstance(sample_field, float):
            self.step = (self.max - self.min) / 100
        else:
            self.step = 1

    def generate_component(self):
        children = html.Div(
            children=[
                self.generate_label_div(),
                dcc.RangeSlider(
                    id=self.name,
                    count=1,
                    min=self.min,
                    max=self.max,
                    step=self.step,
                    value=self.value,
                    marks=self.marks,
                )],
            id=self.parent,
            className='slider-component',
        )

        return self.generate_wrapper(children)

    def get_label(self):
        lower = self.value[0]
        upper = self.value[1]

        if isinstance(self.value[0], float) or isinstance(self.value[1], float):
            lower = '%.3E' % lower
            upper = '%.3E' % upper

        return '{0} is {1}, {2}'.format(self.mongo, lower, upper)

    def __str__(self):
        return str({
            'type': Slider.type,
            'name': self.name,
            'min_val': self.marks,
            'max_val': self.marks,
            'step': self.step,
            'marks': self.marks
        })



