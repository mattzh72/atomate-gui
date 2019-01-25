import collections

class CollectionManager:
    def __init__(self, collection):
        self.collection = collection
        self.metadata = {
            'bools': {},
            'nums': {},
            'lists': {},
            'strings': {},
        }

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
                    self.metadata['nums'][name] = value
                elif isinstance(value, bool):
                    self.metadata['bools'][name] = value
                elif isinstance(value, str):
                    self.metadata['strings'][name] = value
                elif isinstance(value, list):
                    self.metadata['lists'][name] = value

        self.metadata['nums'] = dict.fromkeys(self.metadata['nums'].keys(), [float('inf'), float('-inf')])

        for post in self.collection.find():
            for name, value in self.metadata['nums'].items():
                try:
                    current_val = eval("post" + name)

                    if current_val:
                        if current_val > value[1]:
                            self.metadata['nums'][name] = [value[0], current_val]
                        elif current_val < value[0]:
                            self.metadata['nums'][name] = [current_val, value[1]]

                except KeyError:
                    pass
