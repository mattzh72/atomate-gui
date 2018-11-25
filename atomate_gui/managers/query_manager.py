class QueryManager():
    def __init__(self):
        self.base_query = "{{ '$and': {0} }}"
        self.queries = None
        self.query_templates = {
            "slider": "{{'{0}': {{'$gte': {1}, '$lte': {2}}} }}",
            "input": "{{ '{0}': '{1}' }}",
            "exists": "{{ '{0}': {{ '$exists': 'true' }} }}",
            "hidden": "@HIDDEN",
        }

    def create_query(self, children):
        queries = []

        for child in children:
            val = child['props']['children'][0]['props']['value']
            display = child['props']['style']['display']
            name = child['props']['children'][0]['props']['id']
            name = name.replace("']['", ".").replace("['", "").replace("']", "")
            if display == 'block':
                if isinstance(val, list):
                    queries.append(self.query_templates["slider"].format(name, val[0], val[1]))
                elif isinstance(val, str):
                    queries.append(self.query_templates["input"].format(name, val))

        return self.base_query.format(queries)
