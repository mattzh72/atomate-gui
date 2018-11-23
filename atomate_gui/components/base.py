class BaseComponent:
    type = 'base'

    def __init__(self, name):
        self.name = name
        self.class_name = self.name + "-" + self.type
        self.output_div_name = self.name + '-output-container'

