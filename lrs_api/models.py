from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from dateutil import parser
import uuid
import json
from lrs_api.exceptions import (InvalidStatementJsonException,
                                MissingCaliperFieldException,
                                MissingXAPIFieldException,
                                MissingXAPIAttributeException,
                                StatementExistsException,
                                InvalidContextException,
                                InvalidStatementDateTimeException)


CALIPER_1_1_CONTEXT = "http://purl.imsglobal.org/ctx/caliper/v1p1"


class Tenant(models.Model):
    # Largely undefined.  Tenant code is unimplemented, but i wanted
    # The other table to be able to have their foreign keys established to a
    # default tenant.
    name = models.CharField(max_length=128)


class User(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT)


# Create your models here.
class Statement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    statement = models.TextField()
    verb = models.CharField(max_length=500, db_index=True)
    timestamp = models.DateTimeField(db_index=True, default=timezone.now)
    voided = ''
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True,
                             db_index=True)

    @classmethod
    def validate_unique(cls, uuid):
        try:
            Statement.objects.get(id=uuid)
            msg = "UUID '%s' already exists" % uuid
            raise StatementExistsException(msg)
        except Statement.DoesNotExist:
            pass

    @classmethod
    def from_xapi(cls, tenant, data, json_string):
        new_statement = Statement()
        if "id" in data:
            statement_id = data["id"]
            cls.validate_unique(statement_id)

            new_statement.id = statement_id

        if "verb" not in data:
            raise MissingXAPIAttributeException("verb is required")

        if "id" not in data["verb"]:
            raise MissingXAPIFieldException("id is required for verb")
        verb = data["verb"]["id"]
        new_statement.verb = verb
        new_statement.tenant = tenant
        new_statement.statement = json_string

        new_statement.save()
        return new_statement

    @classmethod
    def from_caliper(cls, tenant, data, json_string):
        new_statement = Statement()
        if "uuid" in data:
            statement_id = data["uuid"]
            cls.validate_unique(statement_id)
            new_statement.id = statement_id

        if "action" not in data:
            raise MissingCaliperAttributeException("action is required")

        if "eventTime" in data:
            try:
                new_statement.timestamp = parser.parse(data["eventTime"])
            except ValueError:
                raise InvalidStatementDateTimeException(data["eventTime"])
        new_statement.verb = data["action"]
        new_statement.tenant = tenant
        new_statement.statement = json_string
        new_statement.save()
        return new_statement

    @classmethod
    def from_json(cls, tenant, json_string):
        try:
            data = json.loads(json_string)
        except ValueError:
            raise InvalidStatementJsonException("Unable to parse JSON")

        if "@context" in data:
            if data["@context"] == CALIPER_1_1_CONTEXT:
                return cls.from_caliper(tenant, data, json_string)
            else:
                raise InvalidContextException(data["@context"])

        else:
            return cls.from_xapi(tenant, data, json_string)
