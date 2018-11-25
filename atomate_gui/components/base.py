class BaseComponent:
    type = 'base'

    def __init__(self, name, active):
        self.name = name
        self.active = active
        self.class_name = self.name + "-" + self.type
        self.mongo_name = name.replace("']['", ".").replace("['", "").replace("']", "")
        self.output_div_name = self.name + '-output-container'
        self.query_templates = {
            "slider": "{{'{0}': {{'$gte': {1}, '$lte': {2}}} }}",
            "input": "{{ '{0}': '{1}' }}",
            "exists": "{{ '{0}': {{ '$exists': 'true' }} }}",
            "hidden": "@HIDDEN",
        }

    def generate_query(self, name, val):
        mongo_name = name.replace("']['", ".").replace("['", "").replace("']", "")
        if isinstance(val, list):
                return self.query_templates["slider"].format(mongo_name, val[0], val[1])
        elif isinstance(val, str):
            if val:
                return self.query_templates["input"].format(mongo_name, val)
            else:
                return self.query_templates["hidden"]
