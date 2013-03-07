from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from .views import ThreadList, ThreadDetail, ThreadCreate

urlpatterns = patterns('', 
                url(r'^topics/$', ThreadList.as_view(), name="list"),
                url(r'^create/$', ThreadCreate.as_view(), name="create"),
                url(r'^thread/(?P<thread_id>\d+)/$', ThreadDetail.as_view(), name="view")
            )