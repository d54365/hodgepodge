from django.test import TestCase

from common.utils.json import JsonUtil


class JsonUtilTestCase(TestCase):
    def test_dumps(self):
        data = {"key": "value"}
        json_data = JsonUtil.dumps(data)
        self.assertEqual(json_data, '{"key": "value"}')

    def test_loads(self):
        json_data = '{"key": "value"}'
        data = JsonUtil.loads(json_data)
        self.assertEqual(data, {"key": "value"})
