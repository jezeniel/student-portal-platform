from django.conf.urls import url, patterns

from .views import create_room, join_room, end_room
urlpatterns = patterns('',
                      url(r'^createroom/(?P<course_id>\d+)$', create_room, name="create"),
                      url(r'^endroom/(?P<course_id>\d+)$', end_room, name="end"),
                      url(r'^joinroom/(?P<course_id>\d+)$', join_room, name="join"),
                      )
