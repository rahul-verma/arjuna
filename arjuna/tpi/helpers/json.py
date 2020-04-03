import json
from arjuna.tpi.helpers.types import ArDict
from jsonpath_rw import jsonpath, parse

class Json(ArDict):

    def __init__(self, d=None):
        super().__init__(d)

    def process_key(self, key):
        return key

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as f:
            jobj = json.load(f)
            return Json(jobj)

    @classmethod
    def from_map(cls, map):
        return Json(d)

    def find(self, query):
        jsonpath_expr = parse(query)
        return [match.value for match in jsonpath_expr.find(self.store)]

    def __getitem__(self, query):
        return self.find(query)

    
