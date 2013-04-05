from django.conf.urls import url, patterns

from .views import course_list, course_view, add_student, accept_course_invite, \
                   decline_course_invite, lecture_upload, lecture_delete, quiz_upload
from discussion.views import SubjectThreadList, SubjectThreadCreate, SubjectThreadDetail

urlpatterns = patterns('',
                url(r'^list$', course_list, name="list"),
                url(r'^view/(?P<course_id>\d+)/$', course_view, name="view"),
                url(r'^invite/(?P<course_id>\d+)/$', add_student, name="invite"),
                url(r'^accept/(?P<course_id>\d+)/$', accept_course_invite, name="accept"),
                url(r'^decline/(?P<course_id>\d+)/$', decline_course_invite, name="decline"),

                url(r'^discussion/(?P<course_id>\d+)/$', SubjectThreadList.as_view(), name="discuss_list"),
                url(r'^discussion/create/(?P<course_id>\d+)$', SubjectThreadCreate.as_view(), name="discuss_create"),
                url(r'^discussion/(?P<course_id>\d+)/(?P<thread_id>\d+)$', SubjectThreadDetail.as_view(), name="discuss_view"),

                url(r'^lecture/upload/(?P<course_id>\d+)/$', lecture_upload, name="upload"),
                url(r'^lecture/delete/(?P<lecture_id>\d+)/$', lecture_delete, name="delete"),
                url(r'^quiz/upload/(?P<course_id>\d+)/$', quiz_upload, name="quiz_upload"),

              )
