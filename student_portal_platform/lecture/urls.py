from django.conf.urls import url, patterns

from .views import create_lecture

urlpatterns = patterns('',
                url(r'^create$', create_lecture, name="create"),
              )
