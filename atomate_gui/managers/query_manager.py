import ast


class QueryManager():
    def __init__(self):
        self.base_query = "{{ '$and': {0} }}"
        self.queries = None
        self.query_templates = {
            "slider": "{{'{0}': {{'$gte': {1}, '$lte': {2}}} }}",
            "input": "{{'{0}': '{1}' }}",
            "exists": "{{ '{0}': {{ '$exists': 'true' }} }}",
            "hidden": "@HIDDEN",
        }

    def create_query(self, names, values, styles):
        queries = []

        for name, value, style in zip(names, values, styles):
            if style['display'] == 'block':
                m_name = name.replace("']['", ".").replace("['", "").replace("']", "")
                if isinstance(value, list):
                    queries.append(ast.literal_eval(self.query_templates["slider"].format(m_name, value[0], value[1])))
                elif isinstance(value, str):
                    if value:
                        queries.append(ast.literal_eval(self.query_templates["input"].format(m_name, value)))
                    else:
                        queries.append(ast.literal_eval(self.query_templates["exists"].format(m_name, value)))

        return "{{ '$and': {0} }}".format(queries)

