from django.contrib import admin

from .models import Thread, Category, SubjectThread


admin.site.register([Thread, Category, SubjectThread])
