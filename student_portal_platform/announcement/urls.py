from django.conf.urls import patterns, url

from announcement import views

urlpatterns = patterns('',
    url(r'^post/$', views.announcement_post , name = "announce_post"),
    url(r'^(?P<post_id>\d+)/', views.announcement_view),                       
)