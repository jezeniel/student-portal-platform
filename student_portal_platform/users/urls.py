from django.conf.urls import url, patterns

from .views import register, editprofile, editaccount
urlpatterns = patterns('',
        url(r'^register/', register, name= 'register_url'),
        url(r'^editprofile/$', editprofile, name="editprofile"),
        url(r'^editaccount/$', editaccount, name='editaccount'),
    )
