from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from lrs_api.views import (ProcessStatement, RecentActivities,
                           TotalActivities, TopActivities)


v1_urlpatterns = [
    url(r'statements$', csrf_exempt(ProcessStatement.as_view()),
        name="lrs_api_statement"),
    url(r'user/recentactivities$', RecentActivities.as_view()),
    url(r'user/totalactivities$', TotalActivities.as_view()),
    url(r'user/topactivities$', TopActivities.as_view()),
]

urlpatterns = [
    url(r'^v1/', include(v1_urlpatterns))
]
