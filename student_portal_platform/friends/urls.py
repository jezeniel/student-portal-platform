from django.conf.urls import url, patterns

from .views import friends, addfriend
urlpatterns = patterns('',
                url(r'^$', friends, name = "list"),
                url(r'^addfriend/(?P<user_id>\d+)/$', addfriend, name = "addfriend"),
            )