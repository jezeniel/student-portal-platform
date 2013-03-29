from django.conf.urls import url, patterns

from .views import send_message, inbox_view, sent_view, message_view

urlpatterns = patterns('',
                url(r'^sendmessage/(?P<user_id>\d+)$', send_message, name="send"),
                url(r'^inbox/$', inbox_view, name="inbox"),
                url(r'^sent/$', sent_view, name="sent"),
                url(r'^(?P<message_id>\d+)$', message_view, name="message"),
            )
