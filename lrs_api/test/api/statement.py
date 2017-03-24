from django.test import Client
from django.urls import reverse
from lrs_api.models import Statement
from lrs_api.test import LRSTest
from lrs_api.test import decode_json as json


class TestStatementAPI(LRSTest):
    def test_methods(self):
        url = reverse("lrs_api_statement")

        client = Client()
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

    def test_bad_post(self):
        url = reverse("lrs_api_statement")
        client = Client()

        response = client.post(url, "", content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_caliper_post(self):

        statement = self.load_statement('caliper', 'quizSubmitted.json')

        url = reverse("lrs_api_statement")

        client = Client()

        Statement.objects.all().delete()
        response = client.post(url, statement, content_type="application/json")

        self.assertEquals(response.status_code, 201)

        all_statements = Statement.objects.all()
        self.assertEquals(len(all_statements), 1)
        s0 = all_statements[0]

    def test_caliper_gets(self):
        Statement.objects.all().delete()
        url = reverse("lrs_api_statement")
        client = Client()

        for name in ['quizSubmitted.json', 'attachmentCreated.json']:
            statement = self.load_statement('caliper', name)
            response = client.post(url, statement,
                                   content_type="application/json")

        response = client.get(url)
        self.assertEquals(response.status_code, 400)

        response = client.get(url, {"since": "2016-10-11T00:00:28.000Z"})
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 2)

        response = client.get(url, {"since": "2016-10-11T00:01:28.000Z"})
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)

        response = client.get(url, {"since": "2016-10-11T00:00:28.000Z",
                                    "limit": 1})
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)

        uuid = '2c3d1836-c610-4a00-a81a-ee2add863e02'
        response = client.get(url, {'uuid': uuid})
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)

        bad_uuid = '2c3d1836-c610-4a00-a81a-ee2add863e00'
        response = client.get(url, {'uuid': bad_uuid})
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 0)
