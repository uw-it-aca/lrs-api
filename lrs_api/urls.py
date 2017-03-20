from django.conf.urls import url
from lrs_api.views import (ProcessStatement, RecentActivities,
                           TotalActivities, TopActivities)


urlpatterns = [
    url(r'statements$', ProcessStatement().run, name="lrs_api_statement"),
    url(r'user/recentactivities$', RecentActivities().run),
    url(r'user/totalactivities$', TotalActivities().run),
    url(r'user/topactivities$', TopActivities().run),
]
