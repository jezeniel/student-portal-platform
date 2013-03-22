from django.conf.urls import url, patterns

from .views import send_message

urlpatterns = patterns('',
                url(r'^sendmessage/(?P<user_id>\d+)$', send_message, name="send"),
                       
                    
            )