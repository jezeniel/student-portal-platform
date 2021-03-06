from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns #remove after development

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'login.views.login_view', name = 'login_url'),
    url(r'^logout/', 'login.views.logout_view', name= 'logout_url'),

    url(r'^home/', 'userprofile.views.home_view', name = 'home_url'),
    url(r'^users/(?P<username>[a-zA-Z0-9]+)', 'userprofile.views.profile_view', name='profile_url'),
    url(r'^search/', 'userprofile.views.search_user', name="search"),
    url(r'^profile/comment/(?P<user_id>\d+)$','userprofile.views.profile_comment', name="profilecomment"),

    url(r'^register/', 'users.views.register', name= 'register_url'),
    url(r'^editprofile/$', 'users.views.editprofile', name="editprofile"),
    url(r'^editaccount/$', 'users.views.editaccount', name='editaccount'),
    url(r'^forgetpass/$', 'users.views.forget_password', name='forgetpass'),
    url(r'^newpassword/(?P<code>[a-zA-Z0-9]+)$', 'users.views.forget_new_password', name="forgetnewpass"),

    url(r'^announcement/', include('announcement.urls', namespace="announcement")),

    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^discussion/', include('discussion.urls', namespace="discuss")),

    url(r'^friends/', include('friends.urls', namespace="friend")),
    url(r'^message/', include('messaging.urls', namespace="message")),
    url(r'^course/', include('subject.urls', namespace="course")),
    url(r'^conference/', include('bbb.urls', namespace="conference")),
    url(r'^lecture/', include('lecture.urls', namespace="lecture")),

    url(r'^quiz/', include('quiz.urls', namespace="quiz")),

    url(r'^usersearch/$', 'search.views.search', name ="usersearch")
)

#remove after development
urlpatterns +=  staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
