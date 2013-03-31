from django.contrib import admin

from .models import Message, Conversation

admin.site.register([Message, Conversation])
