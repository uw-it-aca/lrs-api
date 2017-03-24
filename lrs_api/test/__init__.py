from unittest2 import TestCase
import os
import json


class LRSTest(TestCase):
    def load_statement(self, *path):
        file_path = os.path.join(os.path.dirname(__file__), 'content', *path)
        with open(file_path) as handle:
            return handle.read()


class decode_json(object):
    @classmethod
    def loads(cls, data):
        return json.loads(data.decode("utf-8"))
