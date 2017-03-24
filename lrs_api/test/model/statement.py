from unittest2 import TestCase
from lrs_api.models import Statement, Tenant
import uuid
from lrs_api.exceptions import (InvalidStatementJsonException,
                                MissingXAPIFieldException,
                                MissingXAPIAttributeException,
                                StatementExistsException)


class TestStatementModel(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.get(pk=1)

    def test_empty_json(self):
        with self.assertRaises(InvalidStatementJsonException):
            Statement.from_json(self.tenant, "")

    def test_invalid_json(self):
        with self.assertRaises(InvalidStatementJsonException):
            Statement.from_json(self.tenant, "{ 'ok")

    def test_uuid_block(self):
        uuid_val = uuid.uuid4()
        json = ('{"id": "%s", "verb": { '
                '"id": "http://xapi.org/action" } }') % uuid_val

        s1 = Statement.from_json(self.tenant, json)

        with self.assertRaises(StatementExistsException):
            s2 = Statement.from_json(self.tenant, json)

    def test_missing_verb(self):
        with self.assertRaises(MissingXAPIAttributeException):
            Statement.from_json(self.tenant, "{}")

        with self.assertRaises(MissingXAPIFieldException):
            Statement.from_json(self.tenant, '{"verb":{"missing":"an id" }}')
