from django.http import HttpResponse
from lrs_api.util import require_app_write, require_app_read
from lrs_api.models import Tenant, Statement
from lrs_api.exceptions import InvalidXAPIException


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
        except InvalidXAPIException:
            return HttpResponse(status=400)
        return HttpResponse(status=201)


class RecentActivities(REST):
    pass


class TotalActivities(REST):
    pass


class TopActivities(REST):
    pass
