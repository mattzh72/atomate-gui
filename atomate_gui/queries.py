def generate_slider_query(name, min_val, max_val):
    return "{{'{0}': {{'$gte': {1}, '$lte': {2}}}}}".format(name, min_val, max_val)
