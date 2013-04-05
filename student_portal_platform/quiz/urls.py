from django.conf.urls import url, patterns

from .views import quiz_view, quiz_delete

urlpatterns = patterns('',
                    url(r'^(?P<quiz_id>\d+)$', quiz_view, name="view"),
                    url(r'^delete/(?P<quiz_id>\d+)$', quiz_delete, name="delete")

            )
