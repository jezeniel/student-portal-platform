from django.conf.urls import url, patterns
from .views import ThreadList, ThreadDetail, ThreadCreate, CategoryList

urlpatterns = patterns('',
                       url(r'^$', CategoryList.as_view(), name="category"),
                       url(r'^(?P<category>[a-z-]+)/$', ThreadList.as_view(), name="list"),
                       url(r'^(?P<category>[a-z-]+)/create/$', ThreadCreate.as_view(), name="create"),
                       url(r'^(?P<category>[a-z-]+)/(?P<thread_id>\d+)/$', ThreadDetail.as_view(), name="view"),
                       )
