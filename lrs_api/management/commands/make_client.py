from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
from oauth2_provider.settings import oauth2_settings
from lrs_api.models import OAuthClientWithScopes


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--name', help='Name of the client', required=True)
        parser.add_argument('--write-access',
                            help='Lets the client add events',
                            action='store_true')

    def handle(self, *args, **options):
        ao = Application.objects
        app = ao.create(skip_authorization=True,
                        client_type='confidential',
                        authorization_grant_type='client-credentials',
                        name=options['name'])

        if options['write_access']:
            o = OAuthClientWithScopes.objects
            wrapped = o.create(app_pk=app.pk, granted_scopes='add_records')
        print("ID:%s SECRET:%s" % (app.client_id, app.client_secret))
