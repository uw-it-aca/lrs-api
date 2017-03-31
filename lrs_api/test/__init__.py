from unittest2 import TestCase
import os
import json
from oauth2_provider.models import AccessToken, Application
from oauth2_provider.settings import oauth2_settings
from datetime import datetime, timedelta
from django.utils import timezone


class LRSTest(TestCase):
    valid_read_token = None
    valid_write_token = None
    read_app = None
    write_app = None

    def _get_read_app(self):
        if LRSTest.read_app is None:
            app = Application.objects.create(skip_authorization=True,
                                             name="test_app_read")
            LRSTest.read_app = app
        return LRSTest.read_app

    def _get_write_app(self):
        if LRSTest.write_app is None:
            app = Application.objects.create(skip_authorization=True,
                                             name="test_app_write")
            LRSTest.write_app = app
        return LRSTest.write_app

    def _get_read_header(self):
        if LRSTest.valid_read_token is None:
            app = self._get_read_app()
            read = oauth2_settings.READ_SCOPE
            expires = timezone.now() + timedelta(hours=1)
            token = AccessToken.objects.create(application=app,
                                               scope=read,
                                               token="AA1234",
                                               expires=expires)
            LRSTest.valid_read_token = token.token
        return {"Authorization": "Bearer %s" % LRSTest.valid_read_token}

    def _get_write_header(self):
        if LRSTest.valid_write_token is None:
            app = self._get_write_app()
            write = oauth2_settings.WRITE_SCOPE
            expires = timezone.now() + timedelta(hours=1)
            token = AccessToken.objects.create(application=app,
                                               scope=write,
                                               token="BB543",
                                               expires=expires)
            LRSTest.valid_write_token = token.token
        return {"Authorization": "Bearer %s" % LRSTest.valid_write_token}

    def load_statement(self, *path):
        file_path = os.path.join(os.path.dirname(__file__), 'content', *path)
        with open(file_path) as handle:
            return handle.read()


class decode_json(object):
    @classmethod
    def loads(cls, data):
        return json.loads(data.decode("utf-8"))
