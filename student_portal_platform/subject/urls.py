from django.conf.urls import url, patterns

from .views import course_list, course_view

urlpatterns = patterns('',
                url(r'^list$', course_list, name="list"),
                url(r'^view/(?P<course_id>\d+)/$', course_view, name="view"),
              )
