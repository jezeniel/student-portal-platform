from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns #remove after development

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'student_portal_platform.views.home', name='home'),
    # url(r'^student_portal_platform/', include('student_portal_platform.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'login.views.login_view', name = 'login_url'),
    url(r'^home/' , 'userprofile.views.home_view', name = 'home_url'),
    url(r'^(?P<user_id>\d+)', 'userprofile.views.profile_view', name = 'profile_url'),
    url(r'^logout/', 'login.views.logout_view', name= 'logout_url'),
    url(r'^register/', 'users.views.register', name= 'register_url'),
    url(r'^announcement/', include('announcement.urls', namespace="announcement")),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^quiz/(?P<quiz_id>\d+)/$', 'quiz.views.quiz_view', name = 'quiz_url'),
    url(r'^discussion/', include('discussion.urls', namespace="discuss")),
    url(r'^friends/', include('friends.urls', namespace="friend")),

)

#remove after development
urlpatterns +=  staticfiles_urlpatterns()
