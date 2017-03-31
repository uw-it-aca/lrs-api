from django.conf.urls import url
from lrs_api.views import (ProcessStatement, RecentActivities,
                           TotalActivities, TopActivities)


urlpatterns = [
    url(r'statements$', ProcessStatement.as_view(), name="lrs_api_statement"),
    url(r'user/recentactivities$', RecentActivities.as_view()),
    url(r'user/totalactivities$', TotalActivities.as_view()),
    url(r'user/topactivities$', TopActivities.as_view()),
]
