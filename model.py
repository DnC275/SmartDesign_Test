import json
from bson import ObjectId


class Product:
    def __init__(self, id: ObjectId, title, description='', parameters={}):
        self.id = id
        self.title = title
        self.description = description
        self.parameters = parameters

    def to_json(self):
        return json.dumps(self.json_format(), indent=2)

    def get_id(self) -> ObjectId:
        return self.id

    def json_format(self):
        return {'id': str(self.id), 'title': self.title, 'description': self.description, 'parameters': self.parameters}
