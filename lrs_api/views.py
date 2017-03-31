from django.http import HttpResponse
from django.views.generic import View
from dateutil import parser
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.views.mixins import (ProtectedResourceMixin,
                                          ReadWriteScopedResourceMixin)
from lrs_api.models import Tenant, Statement
from lrs_api.exceptions import InvalidStatementException


class REST(ProtectedResourceView):
    pass


class ProcessStatement(ReadWriteScopedResourceMixin, ProtectedResourceView):
    def post(self, request):
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
