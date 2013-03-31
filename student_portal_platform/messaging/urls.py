from django.conf.urls import url, patterns

from .views import send_message, inbox_view, sent_view, conversation_view

urlpatterns = patterns('',
                url(r'^sendmessage/(?P<user_id>\d+)$', send_message, name="send"),
                url(r'^inbox/$', inbox_view, name="inbox"),
                url(r'^sent/$', sent_view, name="sent"),
                url(r'^conversation/(?P<conversation_id>\d+)$', conversation_view, name="conversation"),
            )
