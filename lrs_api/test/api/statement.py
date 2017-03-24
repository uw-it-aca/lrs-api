from django.test import Client
from django.urls import reverse
from lrs_api.models import Statement
from lrs_api.test import LRSTest
from lrs_api.test import decode_json as json


class TestStatementAPI(LRSTest):
    def _load_useful(self):
        Statement.objects.all().delete()
        url = reverse("lrs_api_statement")
        client = Client()

        for name in ['quizSubmitted.json', 'attachmentCreated.json']:
            statement = self.load_statement('caliper', name)
            response = client.post(url, statement,
                                   content_type="application/json")

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

        statement = self.load_statement('xapi', 'hang_gliding.json')

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
        self._load_useful()
        url = reverse("lrs_api_statement")
        client = Client()

        response = client.get(url)
        self.assertEquals(response.status_code, 400)

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

    def test_caliper_get_since(self):
        self._load_useful()
        url = reverse("lrs_api_statement")
        client = Client()
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

    def test_caliper_get_until(self):
        self._load_useful()
        url = reverse("lrs_api_statement")
        client = Client()
        response = client.get(url, {"until": "2016-11-11T00:00:28.000Z"})
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 2)

        response = client.get(url, {"until": "2015-10-11T00:01:28.000Z"})
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 0)

        response = client.get(url, {"until": "2016-10-11T00:10:28.000Z",
                                    "limit": 1})
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)

    def test_caliper_get_range(self):
        self._load_useful()
        url = reverse("lrs_api_statement")
        client = Client()
        response = client.get(url, {"until": "2016-10-11T00:00:38.000Z",
                                    "since": "2016-10-11T00:00:08.000Z"})
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)

        self.assertEquals(data[0]["uuid"],
                          "2c3d1836-c610-4a00-a81a-ee2add863e02")

    def test_bad_date_formats(self):
        self._load_useful()
        url = reverse("lrs_api_statement")
        client = Client()
        response = client.get(url, {"until": "2016-1a"})
        self.assertEquals(response.status_code, 400)

        response = client.get(url, {"since": "2016-1a"})
        self.assertEquals(response.status_code, 400)

    def test_by_verb(self):
        self._load_useful()
        url = reverse("lrs_api_statement")
        client = Client()

        response = client.get(url, {"verb": "Submitted"})
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)

        self.assertEquals(data[0]["uuid"],
                          "ad38dfb7-030b-479e-883e-3ef2dc3e3969")
