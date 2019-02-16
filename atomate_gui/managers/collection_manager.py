import collections


class CollectionManager:
    def __init__(self, collection):
        self.collection = collection
        self.metadata = []

    def flatten_collection(self, d, parent_key='', sep="']['"):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self.flatten_collection(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def set_metadata(self):
        fields = self.flatten_collection(self.collection.find_one())

        for name, value in fields.items():
            if name[0] != "_":
                name = "['" + name + "']"

                if isinstance(value, (float, int)) and not isinstance(value, bool):
                    self.metadata.append({
                        'name': name,
                        'type': int,
                    })
                elif isinstance(value, bool):
                    self.metadata.append({
                        'name': name,
                        'type': bool,
                    })
                elif isinstance(value, str):
                    self.metadata.append({
                        'name': name,
                        'type': str,
                    })

        self.detect_ranges()

    def detect_ranges(self):
        for post in self.collection.find():
            for item in self.metadata:
                if item['type'] is int:
                    try:
                        current_val = eval("post" + item['name'])
                        if current_val:
                            if 'min' in item:
                                item['min'] = min(current_val, item['min'])
                            else:
                                item['min'] = float('inf')

                            if 'max' in item:
                                item['max'] = max(current_val, item['max'])
                            else:
                                item['max'] = float('-inf')
                    except KeyError:
                        pass


