from django.conf.urls import patterns, url

from announcement import views

urlpatterns = patterns('',
    url(r'^post/$', views.announcement_post , name = "post"),
    url(r'^view/(?P<post_id>\d+)/$', views.announcement_view, name = "view"),
    url(r'^list/$', views.announcement_list, name = "list", kwargs = {'page_num' : 1}),
    url(r'^profile/$', views.announcement_profile, name = "profile")                  
)