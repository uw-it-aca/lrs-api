from unittest2 import TestCase
from django.test import Client
from django.urls import reverse
from lrs_api.models import Statement


class TestStatementAPI(TestCase):
    def test_methods(self):
        url = reverse("lrs_api_statement")

        client = Client()
        response = client.get(url)
        self.assertEquals(response.status_code, 405)

        response = client.patch(url)
        self.assertEquals(response.status_code, 405)

        response = client.delete(url)
        self.assertEquals(response.status_code, 405)

    def test_post(self):
        url = reverse("lrs_api_statement")

        client = Client()

        statement = """
{
  "actor": {
    "name": "Sally Glider",
    "mbox": "mailto:sally@example.com"
  },
  "verb": {
    "id": "http://adlnet.gov/expapi/verbs/experienced",
    "display": { "en-US": "experienced" }
  },
  "object": {
    "id": "http://example.com/activities/solo-hang-gliding",
    "definition": {
      "name": { "en-US": "Solo Hang Gliding" }
    }
  }
}"""

        Statement.objects.all().delete()
        response = client.post(url, statement, content_type="application/json")

        self.assertEquals(response.status_code, 201)

        all_statements = Statement.objects.all()
        self.assertEquals(len(all_statements), 1)
        s0 = all_statements[0]

        self.assertEquals(s0.verb,
                          "http://adlnet.gov/expapi/verbs/experienced")
        self.assertEquals(s0.statement, statement)
        self.assertEquals(s0.tenant.id, 1)
