import json


class Place():
    def __init__(self, info):
        self.name = info['name']
        coordinates_str = info['coordinates']
        coordinates = []
        for cdt_str in coordinates_str:
            coordinates.append(float(cdt_str))

        self.coordinates = coordinates

    def to_json(self):
        return json.dumps(self.to_obj(), indent=2)

    def to_obj(self):
        return {
            'name': self.name,
            'coordinates': self.coordinates
        }
