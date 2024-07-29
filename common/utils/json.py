import json


class JsonUtil:
    @staticmethod
    def dumps(value):
        return json.dumps(value)

    @staticmethod
    def loads(value):
        return json.loads(value)


class JSONDecodeError(json.JSONDecodeError):
    pass
