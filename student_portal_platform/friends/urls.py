from django.conf.urls import url, patterns

from .views import friends, addfriend, cancelrequest, unfriend, acceptrequest, declinerequest
urlpatterns = patterns('',
                url(r'^$', friends, name = "list"),
                url(r'^addfriend/(?P<user_id>\d+)/$', addfriend, name = "addfriend"),
                url(r'^cancelrequest/(?P<user_id>\d+)/$', cancelrequest, name = "cancelrequest"),
                url(r'^unfriend/(?P<user_id>\d+)/$', unfriend, name = "unfriend"),
                url(r'^acceptrequest/(?P<user_id>\d+)/$', acceptrequest, name = "acceptrequest"),
                url(r'^declinerequest/(?P<user_id>\d+)/$', declinerequest, name = "declinerequest") 
            )