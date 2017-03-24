from unittest2 import TestCase
import os


class LRSTest(TestCase):
    def load_statement(self, *path):
        file_path = os.path.join(os.path.dirname(__file__), 'content', *path)
        with open(file_path) as handle:
            return handle.read()
