class BaseComponent:
    type = 'base'

    def __init__(self, name, active):
        self.name = name
        self.active = active
        self.class_name = self.name + "-" + self.type
        self.mongo_name = name.replace("']['", ".").replace("['", "").replace("']", "")
        self.output_div_name = self.name + '-output-container'
        self.parent_name = self.name + '-parent-container'
