from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from dateutil import parser
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.views.mixins import (ProtectedResourceMixin,
                                          ReadWriteScopedResourceMixin)
from lrs_api.models import Tenant, Statement, OAuthClientWithScopes
from lrs_api.exceptions import InvalidStatementException
from oauth2_provider.oauth2_validators import OAuth2Validator


class REST(ProtectedResourceView):
    pass


class ProcessStatement(ReadWriteScopedResourceMixin, ProtectedResourceView):
    def post(self, request):
        # Ugh, until this is resolved:
        # https://github.com/evonove/django-oauth-toolkit/pull/395
        if request.META.get('HTTP_AUTHORIZATION', '').startswith('Bearer'):
            token = request.META.get('HTTP_AUTHORIZATION', '')[7:]
            if not OAuth2Validator().validate_bearer_token(token=token,
                                                           scopes=[],
                                                           request=request):
                raise Exception("Invalid token - no user")

            if not request.client:
                raise Exception("Invalid token - no client app")

            try:
                client_pk = request.client.pk
                wrapped = OAuthClientWithScopes.objects.get(app_pk=client_pk)
                scopes = wrapped.granted_scopes.split(' ')
                if "add_records" not in scopes:
                    return HttpResponse("No write access for client",
                                        status=403)
            except OAuthClientWithScopes.DoesNotExist:
                return HttpResponse("No write access for client", status=403)

        tenant = Tenant.objects.get(pk=1)

        try:
            created = Statement.from_json(tenant, request.body.decode("utf-8"))
        except InvalidStatementException as ex:
            return HttpResponse(status=400)
        return HttpResponse(status=201)

    def get(self, request):
        tenant = Tenant.objects.get(pk=1)
        has_valid_query = False

        values = Statement.objects.filter(tenant=tenant)
        if "since" in request.GET:
            try:
                date = parser.parse(request.GET['since'])
            except ValueError:
                return HttpResponse(status=400,
                                    content="Invalid format for since")

            values = values.filter(timestamp__gte=date)
            has_valid_query = True

        if "until" in request.GET:
            try:
                date = parser.parse(request.GET['until'])
            except ValueError:
                return HttpResponse(status=400,
                                    content="Invalid format for until")

            values = values.filter(timestamp__lte=date)
            has_valid_query = True

        if "verb" in request.GET:
            has_valid_query = True
            values = values.filter(verb=request.GET['verb'])

        if "uuid" in request.GET:
            has_valid_query = True
            values = values.filter(id=request.GET['uuid'])

        if not has_valid_query:
            return HttpResponse(status=400,
                                content="Some filter params are required")

        if "limit" in request.GET:
            values = values[:int(request.GET["limit"])]

        statement_jsons = map(lambda x: x.statement, values)

        output = "[%s]" % ",".join(statement_jsons)
        return HttpResponse(output)


class RecentActivities(REST):
    pass


class TotalActivities(REST):
    pass


class TopActivities(REST):
    pass
