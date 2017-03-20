from __future__ import unicode_literals
from django.db import models
import uuid
import json
from lrs_api.exceptions import (InvalidXAPIJsonException,
                                MissingXAPIFieldException,
                                MissingXAPIAttributeException,
                                StatementExistsException)


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
    timestamp = ''
    voided = ''
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True,
                             db_index=True)

    @classmethod
    def from_json(cls, tenant, json_string):
        try:
            data = json.loads(json_string)
        except ValueError:
            raise InvalidXAPIJsonException("Unable to parse JSON")

        new_statement = Statement()
        if "id" in data:
            statement_id = data["id"]
            try:
                Statement.objects.get(id=statement_id)
                msg = "UUID '%s' already exists" % statement_id
                raise StatementExistsException(msg)
            except Statement.DoesNotExist:
                pass

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
