from django.contrib import admin

from .models import Thread, Category


admin.site.register([Thread, Category])
