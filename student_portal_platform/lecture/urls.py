from django.conf.urls import url, patterns


urlpatterns = patterns('',
                url(r'^list$', course_list, name = "list" ),
              )
