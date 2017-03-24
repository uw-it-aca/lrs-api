from django.http import HttpResponse
from dateutil import parser
from lrs_api.util import require_app_write, require_app_read
from lrs_api.models import Tenant, Statement
from lrs_api.exceptions import InvalidStatementException


class REST(object):
    def run(self, request, *args, **named_args):
        request_method = request.META['REQUEST_METHOD'].lower()
        methods = ['get', 'post', 'put']
        for method in methods:
            if method == request_method:
                if hasattr(self, method):
                    func = getattr(self, method)
                    return func(request, *args, **named_args)

        return HttpResponse(status=405)


class ProcessStatement(REST):
    # Post and put statements
    @require_app_write
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
                                    body="Invalid format for since")

            values = values.filter(timestamp__gte=date)
            has_valid_query = True

        if "util" in request.GET:
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
